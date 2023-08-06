# imports from normal python site packages
import sys
import tarfile
import datetime
import time
from itertools import chain
from pathlib import Path
from os import PathLike
from typing import Dict, List, Union, Set, Generator
from . import (
    Entity_key, Repository, Tag, Container_id,
    Container_Name_or_Id, split_image_name, descriptor_image_to_service_image,
    entity_image_to_bssenv_descriptor_image,
    descriptor_labels_to_simple_entities_dict
)
from ..os import exec
from ..const import BSSENV_NAMESPACE, BSSENV_COMPOSEFILE_NAMESPACE, BSSENV_CONFIGMAP_NAMESPACE
from ..entities import ENTITY_TYPES, SimpleService, SimpleConfigMap
from ..logging import debug
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / 'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages
import docker
from docker.utils import kwargs_from_env
from docker.models.images import Image


dclient = docker.from_env(timeout=120)
daclient = docker.APIClient(**kwargs_from_env(), timeout=120)


# NETWORKS >

def network_exists(network_name: str) -> bool:
    networks = dclient.networks.list(names=[network_name], greedy=False)
    for network in networks:
        if network.name == network_name:
            return True
    return False


def create_network(network_name: str, *args, **kwargs) -> None:
    dclient.networks.create(network_name, *args, **kwargs)


def get_network(network_name_or_id: str) -> docker.models.networks.Network:
    return dclient.networks.get(network_name_or_id)


def rm_network(network_name_or_id: str) -> None:
    network = get_network(network_name_or_id)
    for container in network.containers:
        network.disconnect(container, force=True)
    network.remove()

# NETWORKS <


# IMAGES >

def list_images(name: str = None) -> List[Image]:
    return dclient.images.list(name=name)


def list_tags(name: str = None) -> Set[Tag]:
    return set(exec([
        'docker', 'image', 'ls', '--format', '{{.Repository}}:{{.Tag}}', name]).stdout.splitlines())


def repositories(name: str = None) -> Set[str]:
    repositories = set()
    for image in dclient.images.list(name=name):
        for tag in image.tags:
            repositories |= set([tag.split(':', 1)[0]])
    return repositories


def image_exists(image_name: str) -> bool:
    try:
        dclient.images.get(image_name)
    except docker.errors.ImageNotFound:
        return False
    return True


def get_image_registry_data(image_name: str) -> docker.models.images.RegistryData:
    return dclient.images.get_registry_data(image_name)


def get_image(image_name: str) -> docker.models.images.Image:
    return dclient.images.get(image_name)


def pull_image(image_name: str) -> None:
    dclient.images.pull(image_name)


def get_image_labels(image_name: str) -> Dict[str, str]:
    return get_image(image_name).labels


def get_image_tags(image_name: str) -> Set[str]:
    return set(get_image(image_name).tags)


def run_image(image_name: str, command: str = None, **kwargs) -> str:
    return dclient.containers.run(image_name, command, **kwargs)


def remove_image(
        image_name: str, force: bool = False, noprune: bool = True) -> None:
    try:
        return dclient.images.remove(image_name, force=force, noprune=noprune)
    except docker.errors.ImageNotFound:
        pass


def remove_image_tag(image_name: str) -> None:
    # remove just one tag. Do not remove image itself. If this is a last tag
    # and the image is currently in use by some container then it will raise
    # an error. If this is a last image tag and this image is currently unused
    # then this will remove tag and image as well
    # INFO: currently there is no way to remove just a tag but not an image
    # itself if the tag is a last tag on an image:
    # -> https://github.com/moby/moby/issues/41758
    tag = split_image_name(image_name)[3]
    if not tag:
        raise Exception(f'Please provide full image name with tag: {image_name}')
    try:
        return dclient.images.remove(image_name, force=False, noprune=True)
    except Exception:
        pass


def tag_image(image_name: str, tag: str) -> None:
    image = get_image(image_name)
    registry, namespace, repository, tag = split_image_name(tag)
    repository = '/'.join(_ for _ in [registry, namespace, repository] if _ is not None)
    image.tag(repository, tag)


def push_image(image_name: str) -> None:
    registry, namespace, repository, tag = split_image_name(image_name)
    repository = '/'.join(_ for _ in [registry, namespace, repository] if _ is not None)
    dclient.images.push(repository, tag)


def build_image(**kwargs) -> Generator[str, None, None]:
    return daclient.build(**kwargs)


def get_image_size(image_name: str) -> int:
    return get_image(image_name).attrs['Size']


def get_image_virtual_size(image_name: str) -> int:
    return get_image(image_name).attrs['VirtualSize']

# IMAGES <


# CONTAINERS >


def containers(**kwargs) -> List[docker.models.containers.Container]:
    return dclient.containers.list(**kwargs)


def get_container(container: Container_Name_or_Id) -> docker.models.containers.Container:
    if container is None:
        raise Exception('Please provide container name or id')
    return dclient.containers.get(container)


def commit_container(container_name: str, repository: str, tag: str) -> None:
    container = get_container(container_name)
    container.commit(repository=repository, tag=tag)


def create_container(image, command=None, **kwargs) -> Container_id:
    container = daclient.create_container(image, command, **kwargs)
    debug(f'create_container.container_id: {container["Id"]}')
    return container["Id"]


def export_container_path(
        container: Container_Name_or_Id,
        src_path: PathLike,
        dest_dir: PathLike) -> None:
    container = get_container(container)
    src_path = Path(src_path)
    dest_dir = Path(dest_dir)
    tar_dest_path = None
    try:
        tar_dest_path = dest_dir / f'{src_path.name}.tar'
        with open(tar_dest_path, 'wb') as tar:
            bits, stat = container.get_archive(src_path)
            for chunk in bits:
                tar.write(chunk)
        with tarfile.open(tar_dest_path) as tar:
            tar.extractall(dest_dir)
    finally:
        if tar_dest_path is not None and tar_dest_path.is_file():
            tar_dest_path.unlink()


def container_id(container_name: str) -> str:
    return get_container(container_name).id


def container_exists(container_name: str) -> bool:
    try:
        get_container(container_name)
    except docker.errors.NotFound:
        return False
    return True


def container_status(container_name: str) -> str:
    # created, restarting, running, removing, paused, exited, dead,
    # not_existing
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return 'not_existing'
    return container.status


def container_healthcheck(container_name: str) -> str:
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return
    res = daclient.inspect_container(container.name)
    return res.get('State', {}).get('Health', {}).get('Status', None)


def is_stopped_container(container_name: str) -> bool:
    return container_status(container_name) in ['created', 'exited', 'dead', 'not_existing']


def is_running_container(container_name: str) -> bool:
    return container_status(container_name) == 'running'


def is_paused_container(container_name: str) -> bool:
    return container_status(container_name) == 'paused'


def is_healthy_container(container_name: str) -> bool:
    healthcheck = container_healthcheck(container_name)
    if healthcheck is not None:
        return healthcheck == 'healthy'
    else:
        return False


def wait_untill_healthy_container(
        container_name: str, timeout: int = 60) -> None:
    now = datetime.datetime.now()
    end = now + datetime.timedelta(seconds=timeout)
    while True:
        if datetime.datetime.now() > end:
            raise Exception('Timeout occured during waiting for healthy container "{container_name}"')
        if is_healthy_container(container_name):
            return
        time.sleep(1)


def wait_untill_stopped_container(
        container_name: str, timeout: int = 60) -> None:
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return
    try:
        container.wait(timeout=timeout)
    except docker.errors.APIError as exc:
        if exc.status_code != 404:
            raise Exception() from exc


def wait_until_running_container(
        container_name: str, timeout: int = 60) -> None:
    now = datetime.datetime.now()
    end = now + datetime.timedelta(seconds=timeout)
    while True:
        if datetime.datetime.now() > end:
            raise Exception('Timeout occured during waiting for running container "{container_name}"')
        if is_running_container(container_name):
            return
        time.sleep(1)


def start_container(
        container_name: str, wait: bool = True, timeout: int = 60) -> None:
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return
    container.start()
    if wait:
        wait_until_running_container(container_name, timeout=timeout)


def stop_container(
        container_name: str, timeout: int = 60) -> None:
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return
    try:
        container.stop(timeout=timeout)
    except docker.errors.APIError as exc:
        if exc.status_code != 404:
            raise Exception() from exc


def rm_container(
        container_name: str, wait: bool = True, timeout: int = 60) -> None:
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return
    container.stop()
    if wait:
        try:
            container.wait(timeout=timeout)
        except docker.errors.APIError as exc:
            if exc.status_code != 404:
                raise Exception() from exc
    if container_exists(container_name):
        try:
            container.remove(force=True)
        except docker.errors.APIError as exc:
            if exc.status_code not in (409, 404):
                # docker.errors.APIError: 409 Client Error: Conflict ("removal of container 385069d44203eb95efa42508dcfcc175ca4d8af9eba9b36bc84435017b6a6b15 is already in progress")  # noqa: E501
                # docker.errors.NotFound: 404 Client Error: Not Found ("No such container: 419f22998248b967ac63097c8807b2eb070d8c8a8f2a64e76f3a3e7038a92970")  # noqa: E501
                raise Exception() from exc
        if wait:
            try:
                container.wait(timeout=timeout, condition='removed')
            except docker.errors.APIError as exc:
                if exc.status_code != 404:
                    raise Exception() from exc


def container_image(container_name: str) -> docker.models.images.Image:
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return
    return container.image


def container_image_tags(container_name: str) -> Set[str]:
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return
    return set(container.image.tags)


def container_image_labels(container_name: str) -> Dict[str, str]:
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return
    return container.image.labels


def container_labels(container_name: str) -> Dict[str, str]:
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return
    return container.labels


def container_ports(container_name: str) -> Dict[str, List[Dict]]:
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return
    return container.attrs.get('NetworkSettings', {}).get('Ports', {})


def container_envs(container_name: str) -> Dict[str, str]:
    container = None
    try:
        container = get_container(container_name)
    except docker.errors.NotFound:
        return
    return {key: value
            for key, _, value in [_.partition('=') for _ in container.attrs.get('Config', {}).get('Env', [])]}


def container_env(container_name: str, env_name: str) -> str:
    envs = container_envs(container_name)
    return envs[env_name] if envs and env_name in envs.keys() else None


def all_containers_external_ports() -> Set[int]:
    external_ports = set()
    for container in containers(all=True, ignore_removed=True):
        try:
            container.reload()
        except docker.errors.NotFound:
            # skip containers that were removed in the meantime
            continue
        port_bindings = container.attrs.get('HostConfig', {}).get('PortBindings', {}) or {}
        external_ports |= set(
            int(_['HostPort']) for _ in chain.from_iterable(_ for _ in port_bindings.values()))
    return external_ports


def container_exec(
        container_name: str,
        cmd: Union[List, str],
        *args,
        stdout=True,
        stderr=True,
        stdin=False,
        tty=False,
        detach=False,
        environment=None,
        **kwargs):
    container = get_container(container_name)
    if is_running_container(container_name):
        return container.exec_run(
            cmd,
            *args,
            stdout=stdout,
            stderr=stderr,
            stdin=stdin,
            tty=tty,
            detach=detach,
            environment=environment,
            **kwargs)
    else:
        raise Exception(f'Container "{container_name}" is not running. Can\'t exec')


def top_container(container_name: str, *ps_args: str) -> Dict:
    container = get_container(container_name)
    if is_running_container(container_name):
        return container.top(ps_args=ps_args)
    else:
        raise Exception(f'Container "{container_name}" is not running. Can\'t top')


def pause_container(container_name: str) -> None:
    container = get_container(container_name)
    if is_running_container(container_name):
        return container.pause()
    else:
        raise Exception(f'Container "{container_name}" is not running. Can\'t pause')


def unpause_container(container_name: str) -> None:
    container = get_container(container_name)
    if is_paused_container(container_name):
        return container.unpause()
    else:
        raise Exception(f'Container "{container_name}" is not paused. Can\'t unpause')

# CONTAINERS <


# OTHERS >

# Entity_key:
#   abc -> service
#   :abc -> config map
def get_config_maps_for_image(image: str) -> Dict[Entity_key, SimpleConfigMap]:
    config_maps = dict()
    entities = dict()
    try:
        labels = get_image_labels(image)
        debug(f'get_config_maps_for_image.labels: {labels}')
        entities = descriptor_labels_to_simple_entities_dict(labels)
        for entity_key, entity in entities.items():
            if entity.type == ENTITY_TYPES.CONFIGMAP.value:
                entity.image = image
                entity.descriptor_image = image  # config maps images are descriptors images themselves
                config_maps[entity_key] = entity
    except Exception as exc:
        debug(f'docker.get_config_maps_for_image.exc: {exc}')
        return dict()
    return config_maps


# Entity_key:
#   abc -> service
#   :abc -> config map
def get_services_for_descriptor_image(descriptor_image: str) -> Dict[Entity_key, SimpleService]:
    services = dict()
    entities = dict()
    try:
        service_image = descriptor_image_to_service_image(descriptor_image)
        labels = get_image_labels(descriptor_image)
        debug(f'get_services_for_descriptor_image.labels: {labels}')
        entities = descriptor_labels_to_simple_entities_dict(labels)
        for entity_key, entity in entities.items():
            if entity.type == ENTITY_TYPES.SERVICE.value:
                entity.image = service_image
                entity.descriptor_image = descriptor_image
                services[entity_key] = entity
    except Exception as exc:
        debug(f'get_services_for_descriptor_image.exc: {exc}')
        return dict()
    return services


# Entity_key:
#   abc -> service
#   :abc -> config map
def get_services_for_image(image: str) -> Dict[Entity_key, SimpleService]:
    return get_services_for_descriptor_image(entity_image_to_bssenv_descriptor_image(image))


# Entity_key:
#   abc -> service
#   :abc -> config map
def get_entities_for_tag(
        tag: str,
        namespace: Union[None, str] = None) -> Dict[Entity_key, Union[SimpleService, SimpleConfigMap]]:
    if namespace is not None:
        namespace = f'{namespace}/{BSSENV_NAMESPACE}'
    else:
        namespace = BSSENV_NAMESPACE
    entities = dict()
    for image_name in list_tags(f'{namespace}/*/*:{tag}'):
        registry, image_namespace, repository, image_tag = split_image_name(image_name)
        if image_namespace == f'{namespace}/composefile':
            entities = {
                **entities,
                **get_services_for_descriptor_image(image_name)}
        elif image_namespace == f'{namespace}/configmap':
            entities = {
                **entities,
                **get_config_maps_for_image(image_name)}
    return entities


def get_all_bssenv_descriptors_tags() -> Dict[Repository, Set[Tag]]:
    # INFO: it skips images with docker registry prefix!
    count = 0
    tags = dict()
    for image in chain(
            list_images(f'{BSSENV_COMPOSEFILE_NAMESPACE}/*'),
            list_images(f'*/{BSSENV_COMPOSEFILE_NAMESPACE}/*')):
        try:
            for image_name in image.tags:
                count += 1
                if f'{BSSENV_COMPOSEFILE_NAMESPACE}/' in image_name:
                    registry, namespace, repository, tag = split_image_name(image_name)
                    if registry is None \
                            and namespace is not None \
                            and (
                                namespace == BSSENV_COMPOSEFILE_NAMESPACE
                                or namespace.endswith(f'/{BSSENV_COMPOSEFILE_NAMESPACE}')
                                or namespace == BSSENV_CONFIGMAP_NAMESPACE
                                or namespace.endswith(f'/{BSSENV_CONFIGMAP_NAMESPACE}')
                            ):
                        repository = f'{namespace}/{repository}'
                        tags[repository] = tags.get(repository, set()) | {tag}
        except docker.errors.ImageNotFound:
            # skip images that were removed in the meantime
            continue
    return tags

# OTHERS <
