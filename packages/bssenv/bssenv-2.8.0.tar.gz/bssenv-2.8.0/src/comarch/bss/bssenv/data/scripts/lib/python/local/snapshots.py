# imports from normal python site packages
import os
import sys
import io
import re
import uuid
import comarch.bss.bssenv as BSSENV_PKG
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Dict, Union, Set, Literal
from itertools import count
from datetime import datetime
from tempfile import TemporaryDirectory
from copy import deepcopy
from itertools import repeat, chain
from . import install
from . import yaml
from . import services
from . import env
from .docker import dockerClient, dockerRegistry, get_remote_name_for_local_image_name
from .tmp import clean_env_tmp_dir
from .config import config
from .os import fexec, create_dir
from .logging import debug, speak
from .paths import ENV_DIR, ENV_MAIN_LOG_FILE, BSSENV_GLOBAL_TMP_DIR, ENV_TMP_DIR, ENV_CONFIG_MAPS_DIR
from .entities import Service, SERVICE_TYPES, SNAPSHOT_TYPES, CONFIG_MAP_TYPES
from .const import BSSENV_COMPOSEFILE_NAMESPACE
from .regex import is_like

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / 'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages
from docker.models.images import Image


# Snapshot protocol v3:
#
# snapshot/v3/metadata:snap_name - meta data image
# snapshot/v3/environment:05731538-8027-11eb-ad0c-14f6d84921b3
# snapshot/v3/service/backend:05731538-8027-11eb-ad0c-14f6d84921b3
# snapshot/v3/service/dataupgrade:05731538-8027-11eb-ad0c-14f6d84921b3
# snapshot/v3/configmap/backend:05731538-8027-11eb-ad0c-14f6d84921b3
#
# Metadata fields:
#   id = id of a snapshot
#   type - environment / service / config_map
#   date - date of snapshot creation
#   config_map_name - name of a config map being snapshotted
#   service_name - name of a service being snapshotted
#   environment_name - name of an environment being snapshotted
#   images - [a, b, c, d, ...] - all images composing the given snapshot

ENV_NAME = env.name()
PROTOCOL_VERSION = 'v3'
ARCHIVER_VERSION = 'latest'
SNAPSHOT_NAME_REGEX = re.compile(r'[_a-zA-Z0-9]+[_\.\-a-zA-Z0-9]*')
Image_name = str
Snapshot_name = str
Snapshot_id = str


class SnapshotMetadata:
    id: str
    snapshot_name: str
    type: Literal[SNAPSHOT_TYPES.CONFIG_MAP, SNAPSHOT_TYPES.SERVICE, SNAPSHOT_TYPES.ENVIRONMENT]
    date: str
    config_map_name: str
    service_name: str
    environment_name: str
    meta_image: str
    images: Set[str]

    def __str__(self) -> str:
        return f'{{name: {self.snapshot_name}, type: {self.type}, date: {self.date}, images: {self.images}}}'

    def __repr__(self) -> str:
        return self.__str__()


def validate_snapshot_name(snapshot_name: Snapshot_name, raiseexc: bool = True) -> bool:
    if is_like(snapshot_name, SNAPSHOT_NAME_REGEX):
        return True
    else:
        if raiseexc:
            raise Exception(
                f'{snapshot_name} is not a valid snpshot name\n\n'
                f'Valid pattern is: {SNAPSHOT_NAME_REGEX.pattern}\n\n'
                f'- allowed characters: letters, digits, -, _, .\n'
                f'- first character should be a letter or digit or "_"')
        else:
            return False


def new_snapshot_id() -> str:
    return str(uuid.uuid1())


def create_snapshot_metadata_image(
    snapshot_name: Snapshot_name, metadata: Dict[str, Union[str, Set[str]]], is_remote: bool = False
) -> None:
    # # --
    # import zlib
    # import base64
    # data = Path('/home/hubert_tarnacki/Environments/ht_01/docker/composefiles/daemons.yml')  # noqa: E501
    # data = zlib.compress(data.read_bytes())
    # data = base64.b64encode(data)
    # data = data.decode('utf-8')
    # print(f'data: {data}')
    # echo "FROM debian:latest" | docker build --label my_new_label="arbitrary value" -t "debian:latest" -
    # # --
    image_name = f'snapshot/{PROTOCOL_VERSION}/metadata:{snapshot_name}'
    if is_remote:
        image_name = get_remote_name_for_local_image_name(image_name)
    dockerfile = 'FROM scratch'
    dockerfile = io.BytesIO(dockerfile.encode('utf-8'))
    labels = {
        # 'bssenv.descriptor': data,
        'snapshot.id': metadata['id'],
        'snapshot.type': metadata['type'],
        'snapshot.date': metadata['date'],
        **({'snapshot.config_map_name': metadata['config_map_name']} if 'config_map_name' in metadata.keys() else {}),
        **({'snapshot.service_name': metadata['service_name']} if 'service_name' in metadata.keys() else {}),
        **({'snapshot.environment_name': metadata['environment_name']}
            if 'environment_name' in metadata.keys() else {}),
        **{f'snapshot.image-{_[0]}': _[1] for _ in zip(count(), metadata['images'])}
    }
    debug(f'labels: {labels}')
    response = [line for line in dockerClient.build_image(
        fileobj=dockerfile,
        tag=image_name,
        labels=labels,
        rm=True,
        forcerm=True)]
    debug(f'response: {response}')
    return image_name


def get_snapshot_metadata(snapshot_name: Snapshot_name, remote: bool = False) -> SnapshotMetadata:
    image_name = f'snapshot/{PROTOCOL_VERSION}/metadata:{snapshot_name}'
    labels = None
    if remote:
        image_name = get_remote_name_for_local_image_name(image_name)
        labels = dockerRegistry.get_image_labels(image_name)
    else:
        labels = dockerClient.get_image_labels(image_name)
    if labels:
        # import zlib
        # import base64
        # data = labels['bssenv.descriptor']
        # data = data.encode('utf-8')
        # data = base64.b64decode(data)
        # data = zlib.decompress(data)
        # data = data.decode('utf-8')
        # print(f'data2: {data}')
        metadata = SnapshotMetadata()
        metadata.id = labels['snapshot.id']
        metadata.snapshot_name = snapshot_name
        metadata.meta_image = image_name
        metadata.type = labels['snapshot.type']
        metadata.date = labels['snapshot.date']
        metadata.config_map_name = labels.get('snapshot.config_map_name', None)
        metadata.service_name = labels.get('snapshot.service_name', None)
        metadata.environment_name = labels.get('snapshot.environment_name', None)
        metadata.images = {__ for _, __ in labels.items() if _.startswith('snapshot.image-')}
        return metadata


def local_snapshot_exists(snapshot_name: Snapshot_name) -> bool:
    metadata_image_name = f'snapshot/{PROTOCOL_VERSION}/metadata:{snapshot_name}'
    return dockerClient.image_exists(metadata_image_name)


def remote_snapshot_exists(snapshot_name: Snapshot_name) -> bool:
    metadata_image_name = f'snapshot/{PROTOCOL_VERSION}/metadata:{snapshot_name}'
    metadata_image_name = get_remote_name_for_local_image_name(metadata_image_name)
    return dockerRegistry.image_exists(metadata_image_name)


def snapshot_exists(snapshot_name: Snapshot_name, remote: bool = False):
    if remote:
        return remote_snapshot_exists(snapshot_name)
    else:
        return local_snapshot_exists(snapshot_name)


def _get_snapshot_metadata_image_tag_for_local_image(image: Image) -> str:
    for tag in image.tags[::-1]:
        if tag.startswith(f'snapshot/{PROTOCOL_VERSION}/metadata:'):
            return tag.partition(':')[2]


def get_local_snapshots_names() -> Set[str]:
    futures = []
    snapshot_repository = f'snapshot/{PROTOCOL_VERSION}/metadata'
    with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
        for image in dockerClient.list_images(f'{snapshot_repository}:*'):
            futures.append(e.submit(_get_snapshot_metadata_image_tag_for_local_image, image))
    snapshots = set((_ for _ in map(lambda _: _.result(), futures) if _))
    return snapshots


def get_local_snapshots() -> List[SnapshotMetadata]:
    snapshots = list(map(lambda _: get_snapshot_metadata(_), get_local_snapshots_names()))
    return [_ for _ in snapshots if _]


def get_remote_snapshots_names() -> Set[str]:
    snapshot_repository = get_remote_name_for_local_image_name(f'snapshot/{PROTOCOL_VERSION}/metadata')
    snapshot_repository = snapshot_repository.partition('/')[2]
    return dockerRegistry.repository_tags(snapshot_repository)


def get_remote_snapshots() -> List[SnapshotMetadata]:
    futures = []
    with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
        for snapshot in get_remote_snapshots_names():
            futures.append(e.submit(get_snapshot_metadata, snapshot, remote=True))
    snapshots = list(map(lambda _: _.result(), futures))
    return [_ for _ in snapshots if _]


def rm_local_snapshot(snapshot_name: Snapshot_name) -> None:
    if local_snapshot_exists(snapshot_name):
        metadata = get_snapshot_metadata(snapshot_name)
        futures = []
        with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
            for image in {*metadata.images, metadata.meta_image}:
                futures.append(e.submit(dockerClient.remove_image_tag, image))
            for future in as_completed(futures):
                future.result()


def rm_local_snapshots(*snapshot_names: str) -> None:
    if len(snapshot_names) < 1:
        snapshot_names = get_local_snapshots_names()
    futures = []
    with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
        for snapshot in snapshot_names:
            futures.append(e.submit(rm_local_snapshot, snapshot))
        for future in as_completed(futures):
            future.result()


def rm_remote_snapshot(snapshot_name: Snapshot_name) -> None:
    if remote_snapshot_exists(snapshot_name):
        metadata = get_snapshot_metadata(snapshot_name, remote=True)
        futures = []
        with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
            for image in {*metadata.images, metadata.meta_image}:
                futures.append(e.submit(dockerRegistry.remove_image, image))
            for future in as_completed(futures):
                future.result()


def rm_remote_snapshots(*snapshot_names: str) -> None:
    if len(snapshot_names) < 1:
        snapshot_names = get_remote_snapshots_names()
    futures = []
    with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
        for snapshot in snapshot_names:
            futures.append(e.submit(rm_remote_snapshot, snapshot))
        for future in as_completed(futures):
            future.result()


def _build_config_map_snapshot_image_name(config_map_name: str, snapshot_id: Snapshot_id):
    config_map_name = config_map_name.lower()
    repository = f'snapshot/{PROTOCOL_VERSION}/configmap/{config_map_name}'
    snapshot_image = f'{repository}:{snapshot_id}'
    return (snapshot_image, repository, snapshot_id)


def _build_service_snapshot_image_name(service_name: str, snapshot_id: Snapshot_id, is_descriptor: bool = False):
    service_name = service_name.lower()
    repository = \
        f'snapshot/{PROTOCOL_VERSION}/service/{BSSENV_COMPOSEFILE_NAMESPACE}/{service_name}' \
        if is_descriptor else f'snapshot/{PROTOCOL_VERSION}/service/{service_name}'
    snapshot_image = f'{repository}:{snapshot_id}'
    return (snapshot_image, repository, snapshot_id)


def _build_environment_snapshot_image_name(snapshot_id: Snapshot_id):
    return f'snapshot/{PROTOCOL_VERSION}/environment:{snapshot_id}'


def _unescape_url_links(service: Service, composefile_entry: Dict) -> None:
    for label_key in service.labels.keys():
        if label_key.startswith('bssenv.url.'):
            url_unescaped = service.labels[label_key] \
                .replace('$${host}', '${host}') \
                .replace('$${port.', '${port.')
            composefile_entry['labels'] = \
                [_ for _ in service.composefile_entry['labels'] if not _.startswith(f'{label_key}=')]
            composefile_entry['labels'].append(f'{label_key}={url_unescaped}')


def _unescape_command_autocompletion(service: Service, composefile_entry: Dict) -> None:
    if 'bssenv.command.bash.autocompletion' in service.labels.keys():
        autocompletion = service.labels["bssenv.command.bash.autocompletion"]
        autocompletion_unescaped = autocompletion.replace("$$", "$")
        composefile_entry['labels'] = \
            [_ for _ in service.composefile_entry['labels'] if not _.startswith('bssenv.command.bash.autocompletion=')]
        composefile_entry['labels'].append(f'bssenv.command.bash.autocompletion={autocompletion_unescaped}')


def _create_service_descriptor_snapshot(service_name: str, snapshot_id: Snapshot_id) -> str:
    with TemporaryDirectory(dir=ENV_TMP_DIR) as tmp_dir:
        snapshot_image = _build_service_snapshot_image_name(service_name, snapshot_id, True)[0]
        build_context_dir = Path(tmp_dir)
        host_backup_dir = build_context_dir / 'backup'
        create_dir(host_backup_dir)
        dockerfile = build_context_dir / 'Dockerfile.template'
        composefile_path = host_backup_dir / f'{service_name}.yml'
        composefile = dict()
        labels = []
        for service in install.get_installed_services().values():
            if service.name == service_name:
                composefile_entry = deepcopy(service.composefile_entry)
                _unescape_url_links(service, composefile_entry)
                _unescape_command_autocompletion(service, composefile_entry)
                composefile_entry['image'] = None
                if 'container_name' in composefile_entry:
                    composefile_entry['container_name'] = \
                        composefile_entry['container_name'].replace('${BSSENV_NAME}_', '')
                composefile[service.key] = composefile_entry
                labels += list(chain.from_iterable(zip(
                    repeat('--label'),
                    (_.replace('bssenv.', f'bssenv.{service.key}.')
                     for _ in service.composefile_entry.get('labels', []) if _.startswith('bssenv.')))))
        yaml.dict_to_file(composefile, composefile_path)
        archiver_image = get_remote_name_for_local_image_name(f'data_providers/archiver:{ARCHIVER_VERSION}')
        if dockerRegistry.image_exists(archiver_image):
            debug(f'Pull docker image: {archiver_image}')
            dockerClient.pull_image(archiver_image)
        elif not dockerClient.image_exists(archiver_image):
            raise Exception(f'Docker image not found: {archiver_image}')
        debug(f'Get dockerfile from: {archiver_image}')
        fexec([
            'docker', 'run', '--rm',
            '--name', f'{ENV_NAME}_get_archiver_dockerfile',
            '-v', f'{build_context_dir}:/dockerfile',
            archiver_image, 'dockerfile']) \
            >> ENV_MAIN_LOG_FILE
        debug(f'Build image: {snapshot_image}')
        fexec([
            'docker', 'build', '--pull',
            '--build-arg', 'COMPONENT=bssenv service snapshot',
            '-t', snapshot_image,
            *labels,
            '-f', f'{dockerfile}',
            build_context_dir]) \
            >> ENV_MAIN_LOG_FILE
        return snapshot_image


def _retag_data_provider_service_image_to_snapshot_image(
        service_name: str, snapshot_id: Snapshot_id, stdout_prefix: str = '-') -> str:
    snapshot_image, repository, tag = _build_service_snapshot_image_name(service_name, snapshot_id)
    service = next((_ for _ in install.get_installed_services().values() if _.name == service_name))
    if service.main_type == SERVICE_TYPES.DATA_PROVIDER.value:
        speak(f'{stdout_prefix} tag service image: {snapshot_image}')
        debug(f'service.image_sha: {service.image_sha}')
        debug(str(service.composefile_entry))
        dockerClient.tag_image(service.image_sha, snapshot_image)
    return snapshot_image


def _retag_config_map_image_to_snapshot_image(
        config_map_name: str, snapshot_id: Snapshot_id, stdout_prefix: str = '-') -> str:
    snapshot_image = _build_config_map_snapshot_image_name(config_map_name, snapshot_id)[0]
    config_map = install.get_installed_config_maps_entries()[config_map_name]
    speak(f'{stdout_prefix} tag config map image: {snapshot_image}')
    debug(f'config_map.image_sha: {config_map.image_sha}')
    dockerClient.tag_image(config_map.image_sha, snapshot_image)
    return snapshot_image


def _create_service_container_or_image_snapshot(
        service_name: str, snapshot_id: Snapshot_id, stdout_prefix: str = '-') -> str:
    snapshot_image, repository, tag = _build_service_snapshot_image_name(service_name, snapshot_id)
    main_type = services.get_service_main_type(service_name)
    if main_type == SERVICE_TYPES.DAEMON.value:
        service = services.get_service(service_name)
        speak(f'{stdout_prefix} commit service container: {service.container_name}')
        dockerClient.commit_container(service.container_name, repository, tag)
    elif main_type == SERVICE_TYPES.COMMAND.value:
        service = services.get_service(service_name)
        speak(f'{stdout_prefix} tag service image: {snapshot_image}')
        debug(f'service.image_sha: {service.image_sha}')
        debug(str(service.composefile_entry))
        dockerClient.tag_image(service.image_sha, snapshot_image)
    elif main_type == SERVICE_TYPES.DATA_PROVIDER.value:
        build = next(
            (_ for _ in install.get_installed_services().values()
             if _.name == service_name and SERVICE_TYPES.DATA_PROVIDER_BUILD.value in _.types),
            None)
        if build is None:
            exit(f'Service "{service_name}" is of type "{SERVICE_TYPES.DATA_PROVIDER.value}" '
                 f'but "{SERVICE_TYPES.DATA_PROVIDER_BUILD.value}" subservice not found')
        compress = next(
            (_ for _ in install.get_installed_services().values()
             if _.name == service_name and SERVICE_TYPES.DATA_PROVIDER_COMPRESS.value in _.types),
            None)
        clean_env_tmp_dir()
        if compress is not None:
            speak(f'{stdout_prefix} run data provider compression')
            services.start(compress.key)
        speak(f'{stdout_prefix} run data provider build docker image: {snapshot_image}')
        services.start(build.key)
        built_image = os.path.expandvars(build.image)
        dockerClient.tag_image(built_image, snapshot_image)
        dockerClient.remove_image_tag(built_image)
        clean_env_tmp_dir()
    return snapshot_image


def create_service_snapshot(service_name: str, snapshot_name: Snapshot_name) -> None:
    snapshot_id = new_snapshot_id()
    descriptor_snapshot_image = _create_service_descriptor_snapshot(service_name, snapshot_id)
    service_snapshot_image = _create_service_container_or_image_snapshot(service_name, snapshot_id)
    create_snapshot_metadata_image(
        snapshot_name,
        {
            'id': snapshot_id,
            'type': SNAPSHOT_TYPES.SERVICE.value,
            'date': str(datetime.now()),
            'service_name': service_name,
            'images': [descriptor_snapshot_image, service_snapshot_image]
        }
    )


def _create_config_map_snapshot(config_map_name: str, snapshot_id: Snapshot_id) -> str:
    snapshot_image = _build_config_map_snapshot_image_name(config_map_name, snapshot_id)[0]
    config_map = install.get_installed_config_maps_entries()[config_map_name]
    dockerfile = f'''
        FROM scratch
        COPY ./{config_map_name} /config/maps/{config_map_name}
    '''.encode()
    fexec(
        [
            'docker', 'build', '--rm', '--force-rm',
            '-t', snapshot_image,
            '--label', f'bssenv.configmap.{config_map_name}=/config/maps/{config_map_name}',
            *(['--label', 'asEnvs'] if config_map.type == CONFIG_MAP_TYPES.ENV.value else []),
            '-f-',
            str(ENV_CONFIG_MAPS_DIR)
        ],
        input=dockerfile) >> ENV_MAIN_LOG_FILE
    return snapshot_image


def create_config_map_snapshot(config_map_name: str, snapshot_name: Snapshot_name) -> None:
    snapshot_id = new_snapshot_id()
    config_map_snapshot_image = _create_config_map_snapshot(config_map_name, snapshot_id)
    create_snapshot_metadata_image(
        snapshot_name,
        {
            'id': snapshot_id,
            'type': SNAPSHOT_TYPES.CONFIG_MAP.value,
            'date': str(datetime.now()),
            'config_map_name': config_map_name,
            'images': [config_map_snapshot_image]
        }
    )


def create_environment_snapshot(snapshot_name: Snapshot_name) -> None:
    with TemporaryDirectory(dir=BSSENV_GLOBAL_TMP_DIR) as tmp_dir:
        snapshot_id = new_snapshot_id()
        build_context_dir = Path(tmp_dir)
        host_backup_dir = build_context_dir / 'backup'
        create_dir(host_backup_dir)
        dockerfile = build_context_dir / 'Dockerfile.template'
        snapshot_images = set()
        snapshot_image = _build_environment_snapshot_image_name(snapshot_id)
        snapshot_images.add(snapshot_image)
        archiver_image = get_remote_name_for_local_image_name(f'data_providers/archiver:{ARCHIVER_VERSION}')
        if dockerRegistry.image_exists(archiver_image):
            speak(f'- pull docker image: {archiver_image}')
            dockerClient.pull_image(archiver_image)
        elif not dockerClient.image_exists(archiver_image):
            raise Exception(f'Docker image not found: {archiver_image}')
        speak(f'- compress environment directory')
        speak(f'  • environment directory: {ENV_DIR}')
        speak(f'  • build temporary directory: {build_context_dir}')
        fexec([
            'docker', 'run', '--rm',
            '--name', f'{ENV_NAME}_compress_environment',
            '-v', f'{ENV_DIR}:/compress',
            '-v', f'{host_backup_dir}:/backup',
            '-v', f'{build_context_dir}:/dockerfile',
            archiver_image, 'compress']) \
            >> ENV_MAIN_LOG_FILE
        speak(f'- build docker image: {snapshot_image}')
        fexec([
            'docker', 'build', '--pull',
            '--build-arg', 'COMPONENT=bssenv environment snapshot',
            '-t', snapshot_image,
            '-f', f'{dockerfile}',
            build_context_dir]) \
            >> ENV_MAIN_LOG_FILE
    speak(f'- create containers and images snapshots')
    futures = []
    with ThreadPoolExecutor() as e:
        for service in install.get_installed_services().values():
            if service.is_command or service.is_daemon:
                futures.append(e.submit(
                    _create_service_container_or_image_snapshot, service.name, snapshot_id, stdout_prefix='  •'))
            elif service.is_data_provider:
                futures.append(e.submit(
                    _retag_data_provider_service_image_to_snapshot_image, service.name, snapshot_id,
                    stdout_prefix='  •'))
        for config_map in install.get_installed_config_maps_entries().values():
            futures.append(e.submit(
                _retag_config_map_image_to_snapshot_image, config_map.key, snapshot_id, stdout_prefix='  •'))
    snapshot_images |= set(map(lambda _: _.result(), futures))
    create_snapshot_metadata_image(
        snapshot_name,
        {
            'id': snapshot_id,
            'type': SNAPSHOT_TYPES.ENVIRONMENT.value,
            'date': str(datetime.now()),
            'environment_name': ENV_NAME,
            'images': snapshot_images
        }
    )


def _push_one_snapshot_image(image: str) -> str:
    remote_image = get_remote_name_for_local_image_name(image)
    debug(f'Tag image: {image}')
    debug(f'with tag: {remote_image}')
    dockerClient.tag_image(image, remote_image)
    debug(f'Push image: {remote_image}')
    dockerClient.push_image(remote_image)
    dockerClient.remove_image_tag(remote_image)
    return remote_image


def push_snapshot(snapshot_name: Snapshot_name) -> None:
    if local_snapshot_exists(snapshot_name):
        metadata = get_snapshot_metadata(snapshot_name)
        remote_images = []
        with ThreadPoolExecutor(
            max_workers=config.thread.pool.max.workers
        ) as e:
            for image in metadata.images:
                remote_images.append(e.submit(_push_one_snapshot_image, image))
        remote_metadata_image = create_snapshot_metadata_image(
            snapshot_name,
            {
                'id': metadata.id,
                'type': metadata.type,
                'date': metadata.date,
                **(
                    {'config_map_name': metadata.config_map_name}
                    if metadata.type == SNAPSHOT_TYPES.CONFIG_MAP.value else {}),
                **(
                    {'service_name': metadata.service_name}
                    if metadata.type == SNAPSHOT_TYPES.SERVICE.value else {}),
                **(
                    {'environment_name': metadata.environment_name}
                    if metadata.type == SNAPSHOT_TYPES.ENVIRONMENT.value else {}),
                'images': list(map(lambda _: _.result(), remote_images))
            },
            is_remote=True
        )
        dockerClient.push_image(remote_metadata_image)
        dockerClient.remove_image_tag(remote_metadata_image)
    else:
        raise Exception(f'Local snapshot with name "{snapshot_name}" not found')
