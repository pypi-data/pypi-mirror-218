# imports from normal python site packages
import shutil
import sys
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional, Set, Dict, Tuple, Union
from os.path import expandvars
from os import listdir
from . import tmp
from . import ports
from . import switches
from . import uninstall
from . import env
from . import composefile
from . import yaml
from . import os
from . import dns
from . import commands
from . import paths
from .threading import register_cancellable, unregister_cancellable
from .docker import dockerClient, dockerRegistry, entity_image_to_bssenv_descriptor_image, split_image_name
from .itertools import each
from .config import config
from .const import BSSENV_SNAPSHOT_NAMESPACE
from .terminal import Screen
from .regex import is_like
from .entities import Service, SERVICE_TYPES, COMPOSEFILE_TYPES, SimpleService, SimpleConfigMap, \
    InstalledServicesEntry, InstalledConfigMapsEntry, COMMAND_TYPES
from .os import exec
from .logging import debug, info
from .cache import Cache, CacheEntry, CacheTransformer, FileCacheEntry, SharedMultiFileCacheReloader, \
    YamlCacheTransformer
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / 'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from local.os import use_raw_output


lock_installed_services_file = threading.RLock()
lock_installed_config_maps_file = threading.RLock()
INSTALLED_SERVICES_FILE_CACHE = Cache()
INSTALLED_CONFIG_MAPS_FILE_CACHE = Cache()
SERVICES_CACHE = Cache()
COMPOSEFILES_CACHE = Cache()
ENV_INSTALLED_SERVICES_FILE = paths.ENV_INSTALLED_SERVICES_FILE
ENV_INSTALLED_CONFIG_MAPS_FILE = paths.ENV_INSTALLED_CONFIG_MAPS_FILE
ENV_TMP_DIR = paths.ENV_TMP_DIR
ENV_TEMPLATE_SHELL_COMMAND_FILE = paths.ENV_TEMPLATE_SHELL_COMMAND_FILE
ENV_TEMPLATE_SHELL_SERVICE_COMMAND_FILE = paths.ENV_TEMPLATE_SHELL_SERVICE_COMMAND_FILE
Entity_key = str
Config_map_key = str
Service_key = str
Service_name = str
console = Console()


class InstalledConfigMapsFileCacheTransformer(CacheTransformer):

    def transform(self) -> Dict[Config_map_key, InstalledConfigMapsEntry]:
        if self.value is not None:
            entries = [_.split(' | ') for _ in self.value.splitlines() if len(_.strip()) > 0 and _.find(' | ') > -1]
            installed_config_maps = {}
            for entry in entries:
                config_map_key, image_sha, image_name, type = entry
                config_map = InstalledConfigMapsEntry()
                config_map.key = config_map_key
                config_map.image_sha = image_sha
                config_map.image_name = image_name
                config_map.type = type
                installed_config_maps[config_map_key] = config_map
            self.value = installed_config_maps
        else:
            self.value = {}
        return self.value


class InstalledConfigMapsFileCacheEntry(
        InstalledConfigMapsFileCacheTransformer, FileCacheEntry):
    pass


def get_installed_config_maps_entries() -> Dict[Config_map_key, InstalledConfigMapsEntry]:
    with lock_installed_config_maps_file:
        if not INSTALLED_CONFIG_MAPS_FILE_CACHE.exists(ENV_INSTALLED_CONFIG_MAPS_FILE):
            INSTALLED_CONFIG_MAPS_FILE_CACHE.add(InstalledConfigMapsFileCacheEntry(ENV_INSTALLED_CONFIG_MAPS_FILE))
        return INSTALLED_CONFIG_MAPS_FILE_CACHE.get(ENV_INSTALLED_CONFIG_MAPS_FILE)


def get_installed_config_maps_keys() -> Set[Config_map_key]:
    return set(get_installed_config_maps_entries().keys())


# config map name == config map key
def get_installed_config_maps_names() -> Set[Config_map_key]:
    return get_installed_config_maps_keys()


def is_installed_config_map(config_map_key: Config_map_key) -> bool:
    return config_map_key in get_installed_config_maps_keys()


def set_installed_config_maps_entries(
        config_maps: Dict[Config_map_key, InstalledConfigMapsEntry]) -> None:
    with lock_installed_config_maps_file:
        ENV_INSTALLED_CONFIG_MAPS_FILE.write_text(
            "\n".join(f'{_.key} | {_.image_sha} | {_.image_name} | {_.type}' for _ in config_maps.values()) + "\n")


def add_installed_config_maps(config_maps: Dict[Config_map_key, InstalledConfigMapsEntry]) -> None:
    if len(config_maps.keys()) > 0:
        all_config_maps = get_installed_config_maps_entries().copy()  # do not modify cached set directly!
        all_config_maps = {**all_config_maps, **config_maps}
        set_installed_config_maps_entries(all_config_maps)


def remove_installed_config_maps(config_maps_keys: Set[Config_map_key] = None) -> None:
    if config_maps_keys is None:
        with lock_installed_config_maps_file:
            # remove all
            ENV_INSTALLED_CONFIG_MAPS_FILE.write_text('')
    else:
        if len(config_maps_keys) > 0:
            # remove given set
            all_config_maps = get_installed_config_maps_entries().copy()  # do not modify cached set directly!
            for config_map_key in config_maps_keys:
                if config_map_key in all_config_maps.keys():
                    del all_config_maps[config_map_key]
            set_installed_config_maps_entries(all_config_maps)


def remove_installed_config_map(config_map_key: str) -> None:
    remove_installed_config_maps({config_map_key})


class InstalledServicesFileCacheTransformer(CacheTransformer):

    def transform(self) -> Dict[Service_key, InstalledServicesEntry]:
        if self.value is not None:
            entries = [_.split(' | ') for _ in self.value.splitlines() if len(_.strip()) > 0 and _.find(' | ') > -1]
            installed_services = {}
            for entry in entries:
                service_key, service_name, main_type, image_sha, image_name, image_guard_container = entry
                service = InstalledServicesEntry()
                service.key = service_key
                service.name = service_name
                service.type = main_type
                service.image_sha = image_sha
                service.image_name = image_name
                service.image_guard_container = image_guard_container
                installed_services[service_key] = service
            self.value = installed_services
        else:
            self.value = {}
        return self.value


class InstalledServicesFileCacheEntry(
        InstalledServicesFileCacheTransformer, FileCacheEntry):
    pass


def get_installed_services_entries() -> Dict[Service_key, InstalledServicesEntry]:
    with lock_installed_services_file:
        if not INSTALLED_SERVICES_FILE_CACHE.exists(ENV_INSTALLED_SERVICES_FILE):
            INSTALLED_SERVICES_FILE_CACHE.add(InstalledServicesFileCacheEntry(ENV_INSTALLED_SERVICES_FILE))
        return INSTALLED_SERVICES_FILE_CACHE.get(ENV_INSTALLED_SERVICES_FILE)


class ServiceCacheTransformer(CacheTransformer):

    def transform(self) -> Dict[Service_key, Service]:
        if self.value is not None:
            YamlCacheTransformer.transform(self)
            self.value = Service.from_dict(self.service_key, self.value['services'][self.service_key])
        return self.value


class ServiceFileCacheEntry(
        ServiceCacheTransformer, SharedMultiFileCacheReloader, CacheEntry):

    def __init__(
            self,
            service_key: Service_key,
            service_name: Service_name,
            service_type: str):
        CacheEntry.__init__(self, key=service_key)
        SharedMultiFileCacheReloader.__init__(self, cache=COMPOSEFILES_CACHE)
        self.__service_key = service_key
        self.__service_name = service_name
        self.__service_type = service_type

    @property
    def service_key(self) -> str:
        return self.__service_key

    def is_invalidated(self) -> bool:
        service_composefile_path = Path(
            composefile.get_path_for_service_name_composefile(self.__service_name, self.__service_type))
        return SharedMultiFileCacheReloader.is_invalidated(self, path=service_composefile_path)

    def reload(self) -> Union[None, str]:
        service_composefile_path = Path(
            composefile.get_path_for_service_name_composefile(self.__service_name, self.__service_type))
        return SharedMultiFileCacheReloader.reload(self, path=service_composefile_path)


def get_installed_service(service_key: str) -> Service:
    with lock_installed_services_file:
        if not SERVICES_CACHE.exists(service_key):
            installed_services_entries = get_installed_services_entries()
            if service_key not in installed_services_entries.keys():
                raise Exception(f'Service "{service_key}" not found in installed services')
            else:
                installed_services_entry = installed_services_entries[service_key]
                service_name = installed_services_entry.name
                service_type = installed_services_entry.type
                SERVICES_CACHE.add(ServiceFileCacheEntry(service_key, service_name, service_type))
        return SERVICES_CACHE.get(service_key)


def get_installed_services_keys() -> Set[Service_key]:
    return set(get_installed_services_entries().keys())


def get_installed_services_names() -> Set[Service_name]:
    return set(_.name for _ in get_installed_services_entries().values())


def is_installed_service(service_key: str) -> bool:
    return service_key in get_installed_services_keys()


def get_installed_services() -> Dict[Service_key, Service]:
    return {_: get_installed_service(_) for _ in get_installed_services_keys()}


def set_installed_services(services: Dict[Service_key, Service]) -> None:
    with lock_installed_services_file:
        ENV_INSTALLED_SERVICES_FILE.write_text(
            "\n".join(f'{_.key} | {_.name} | {_.main_type} | {_.image_sha} | {_.image_name} | {_.image_guard_container}'
                      for _ in services.values()) + "\n")


def set_installed_services_entries(services: Dict[Service_key, InstalledServicesEntry]) -> None:
    with lock_installed_services_file:
        ENV_INSTALLED_SERVICES_FILE.write_text(
            "\n".join(f'{_.key} | {_.name} | {_.type} | {_.image_sha} | {_.image_name} | {_.image_guard_container}'
                      for _ in services.values()) + "\n")


def add_installed_services(services: Dict[Service_key, Service]) -> None:
    if len(services.keys()) > 0:
        all_services = get_installed_services()  # this always returns new dict. No need to copy
        all_services = {**all_services, **services}
        set_installed_services(all_services)


def remove_installed_services(service_keys: Set[Service_key] = None) -> None:
    if service_keys is None:
        with lock_installed_services_file:
            # remove all
            ENV_INSTALLED_SERVICES_FILE.write_text('')
    else:
        if len(service_keys) > 0:
            # remove given set
            all_services = get_installed_services()  # this always returns new dict. No need to copy
            for service_key in service_keys:
                if service_key in all_services.keys():
                    del all_services[service_key]
            set_installed_services(all_services)


def remove_installed_service(service_key: str) -> None:
    remove_installed_services({service_key})


# Entity_key:
#   abc -> service
#   :abc -> config map
def get_entities_for_tag(
        tag: str,
        namespace: Union[None, str] = None) -> Dict[Entity_key, Union[SimpleService, SimpleConfigMap]]:
    with ThreadPoolExecutor(max_workers=2) as pool:
        remote_future = pool.submit(dockerRegistry.get_entities_for_tag, tag, namespace)
        local_future = pool.submit(dockerClient.get_entities_for_tag, tag, namespace)
        each(as_completed([remote_future, local_future]), lambda _: _.result())
        return {
            **local_future.result(),
            **remote_future.result()  # prefer remote results over local
        }


# Entity_key:
#   abc -> service
#   :abc -> config map
def get_config_maps_for_image(image: str) -> Dict[Entity_key, SimpleConfigMap]:
    with ThreadPoolExecutor(max_workers=2) as pool:
        remote_future = pool.submit(dockerRegistry.get_config_maps_for_image, image)
        local_future = pool.submit(dockerClient.get_config_maps_for_image, image)
        each(as_completed([remote_future, local_future]), lambda _: _.result())
        return {
            **local_future.result(),
            **remote_future.result()  # prefer remote results over local
        }


# Entity_key:
#   abc -> service
#   :abc -> config map
def get_services_for_image(image: str) -> Dict[Entity_key, SimpleService]:
    with ThreadPoolExecutor(max_workers=2) as pool:
        remote_future = pool.submit(dockerRegistry.get_services_for_image, image)
        local_future = pool.submit(dockerClient.get_services_for_image, image)
        each(as_completed([remote_future, local_future]), lambda _: _.result())
        return {
            **local_future.result(),
            **remote_future.result()  # prefer remote results over local
        }


def _pull_image(image: str, cancel: threading.Event, progress: Optional[Progress] = None) -> None:
    if dockerRegistry.image_exists(image):
        info(f"Pulling: {image}")
        if image.startswith('sha256:'):
            image_ctx_id = image
        else:
            *_, repository, tag = split_image_name(image)
            image_ctx_id = f'{repository}:{tag}'
        tasks = dict()
        for line in dockerClient.daclient.pull(image, stream=True, decode=True):
            if cancel.is_set():
                return
            info(f'{image}: {line}')
            if progress and 'id' in line and 'status' in line and 'progressDetail' in line:
                progress_id = line['id']
                status = line['status']
                progress_details = line['progressDetail'] or {}
                current = progress_details.get('current', None)
                total = progress_details.get('total', None)
                if current is not None and total is not None and total > 0:
                    if progress_id in tasks.keys():
                        task_id = tasks[progress_id]
                    else:
                        task_id = progress.add_task(
                            progress_id, start=True, visible=True,
                            total=total, image_ctx_id=image_ctx_id,
                            progress_id=progress_id, status=status)
                        tasks[progress_id] = task_id
                    task = progress._tasks[task_id]
                    progress.update(task_id, completed=current, status=status)
                    if task.finished:
                        progress.remove_task(task_id)
                        del tasks[progress_id]


def pull_images(*images: str) -> None:
    futures = []
    if use_raw_output():
        with ThreadPoolExecutor(max_workers=config.docker.max.pull.workers) as pool:
            cancel = register_cancellable()
            try:
                for image in images:
                    futures.append(pool.submit(_pull_image, image, cancel))
                each(as_completed(futures), lambda _: _.result())
            except Exception as e:
                cancel.set()
                raise e
            finally:
                unregister_cancellable(cancel)
    else:
        with Progress(
            TextColumn("[bold white]{task.fields[image_ctx_id]}", justify="left"),
            TextColumn("[bold green]{task.fields[progress_id]}", justify="left"),
            TextColumn("[bold blue]{task.fields[status]}", justify="left"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
            speed_estimate_period=5,
            transient=True,
            console=console
        ) as progress:
            with ThreadPoolExecutor(max_workers=config.docker.max.pull.workers) as pool:
                cancel = register_cancellable()
                try:
                    for image in images:
                        futures.append(pool.submit(_pull_image, image, cancel, progress))
                    each(as_completed(futures), lambda _: _.result())
                except Exception as e:
                    cancel.set()
                    raise e
                finally:
                    unregister_cancellable(cancel)


def _unpack_composefile_from_image_to_tmp(image: str) -> Path:
    # clean tmp dir
    tmp.clean_env_tmp_dir()
    # unpack composefile to tmp
    debug(f'Unpack composefile from image: {image}')
    exec(["docker", "run", "-v", f"{ENV_TMP_DIR}:/restore", "--rm", image, "restore"])
    # check if at least one composefile exists
    composefile_path = next(ENV_TMP_DIR.iterdir(), None)
    if composefile_path is None:
        raise Exception(f'Composefile not found in docker image: {image}')
    return composefile_path


def _create_command_shell_script(service: Service, command_key: Optional[str] = None) -> None:
    debug(f'_create_command_shell_script: [{service.key}, {command_key}]')
    shell_script_name = None
    if command_key or service.main_type == SERVICE_TYPES.COMMAND.value:
        if command_key:
            cmd = (service.commands or {}).get(command_key, {})
            shell_script_name = cmd.get('generate_script', None)
            if shell_script_name:
                debug(f'Create shell script "{shell_script_name}" for service command"{command_key}"')
                template = ENV_TEMPLATE_SHELL_SERVICE_COMMAND_FILE.read_text()
                shell_script = template \
                    .replace('<SERVICE_KEY>', service.key) \
                    .replace('<COMMAND_KEY>', command_key)
        elif service.main_type == SERVICE_TYPES.COMMAND.value:
            shell_script_name = service.command_shell_name
            if shell_script_name:
                debug(f'Create shell script "{shell_script_name}" for command service"{service.key}"')
                template = ENV_TEMPLATE_SHELL_COMMAND_FILE.read_text()
                shell_script = template.replace('<SERVICE_KEY>', service.key)
    if shell_script_name and shell_script:
        commands.add_shell_script_to_command_registry(service, shell_script_name, shell_script, command_key)


def _install_command_autocompletion(service: Service, command_key: Optional[str] = None) -> None:
    debug(f'_install_command_autocompletion: [{service.key}, {command_key}]')
    shell_script_name, autocompletion_body = None, None
    if command_key:
        cmd = (service.commands or {}).get(command_key, {})
        shell_script_name = cmd.get('generate_script', None)
        autocompletion_body = cmd.get('autocompletion', None)
        if autocompletion_body:
            cmd['autocompletion'] = autocompletion_body.replace("$", "$$")
    elif service.main_type == SERVICE_TYPES.COMMAND.value:
        shell_script_name = service.command_shell_name
        autocompletion_body = service.labels.get("bssenv.command.bash.autocompletion", None)
        if autocompletion_body:
            autocompletion_body_escaped = autocompletion_body.replace("$", "$$")
            service.composefile_entry['labels'] = \
                [_ for _ in service.composefile_entry['labels']
                 if not _.startswith('bssenv.command.bash.autocompletion=')]
            service.composefile_entry['labels'].append(
                f'bssenv.command.bash.autocompletion={autocompletion_body_escaped}'
            )
    if shell_script_name and autocompletion_body:
        commands.add_autocompletion_to_command_registry(service, shell_script_name, autocompletion_body, command_key)


def _add_command_to_command_registry(service: Service, command_key: Optional[str] = None) -> None:
    commands.add_command_to_command_registry(service, command_key)


def _add_service_to_composefile(
        service: Service, service_type: str, composefile_dict: Dict, composefile_name: str) -> None:
    debug(f'Add service "{service.key}" to composefile "{composefile_name}"')
    composefile_dict['services'] = composefile_dict.get('services', None) or {}
    composefile_dict['services'][service.key] = service.composefile_entry
    debug(f'composefile_dict: {composefile_dict}')
    composefile.set_composefile(composefile_dict, composefile_name, service_type)


def _create_host_directories_for_service_volumes(service: Service) -> None:
    for volume in service.composefile_entry.get('volumes', []):
        if is_like(volume, '^[^:]+:[^:]+$'):
            volume = Path(expandvars(volume.split(':')[0]))
            if not volume.exists():
                debug(f'Creating volume host directory: "{volume}"')
                os.create_dir(volume)


def _install_daemon_service(service: Service) -> None:
    composefile_name = 'daemons.yml'
    composefile_dict = composefile.get_composefile(composefile_name, COMPOSEFILE_TYPES.DAEMON.value)
    _add_service_to_composefile(service, SERVICE_TYPES.DAEMON.value, composefile_dict, composefile_name)


def _install_command_service(service: Service) -> None:
    composefile_name = f'{service.name}.yml'
    service.bssenv['command'] = {'uuid': str(uuid.uuid4())}
    _create_command_shell_script(service)
    _install_command_autocompletion(service)
    _add_command_to_command_registry(service)
    composefile_dict = composefile.get_template()
    _add_service_to_composefile(service, SERVICE_TYPES.COMMAND.value, composefile_dict, composefile_name)


def _install_data_provider_service(service: Service) -> None:
    composefile_name = f'{service.name}.yml'
    if service.is_data_provider_builder:
        service.image = \
            f'{BSSENV_SNAPSHOT_NAMESPACE}/{service.name.lower()}:${{BSSENV_NAME}}-{service.name.lower()}-latest'
    if composefile.exists(composefile_name, COMPOSEFILE_TYPES.DATA_PROVIDER.value):
        composefile_dict = composefile.get_composefile(composefile_name, COMPOSEFILE_TYPES.DATA_PROVIDER.value)
    else:
        composefile_dict = composefile.get_template()
    _add_service_to_composefile(service, SERVICE_TYPES.DATA_PROVIDER.value, composefile_dict, composefile_name)


def _escape_url_links(service: Service) -> None:
    for label_key in service.labels.keys():
        if label_key.startswith('bssenv.url.'):
            url_escaped = service.labels[label_key] \
                .replace('${host}', '$${host}') \
                .replace('${port.', '$${port.')
            service.composefile_entry['labels'] = \
                [_ for _ in service.composefile_entry['labels']
                 if not _.startswith(f'{label_key}=')]
            service.composefile_entry['labels'].append(
                f'{label_key}={url_escaped}')


def _install_service_commands(service: Service) -> None:
    for command_key in service.commands.keys():
        info(f"Installing command '{command_key}' from service '{service.key}'")
        service.commands[command_key]['uuid'] = str(uuid.uuid4())
        _create_command_shell_script(service, command_key)
        _install_command_autocompletion(service, command_key)
        _add_command_to_command_registry(service, command_key)


def _install_services_from_composefile(
        composefile: Dict, path: str, service_keys: Set[Service_key], image: str, image_sha: str,
        image_guard_container_sha: str, screen: Screen, progress: Dict[str, Dict]) -> Dict[Service_key, Service]:
    debug(f'Install services from composefile: {path}')
    services = {_.key: _ for _ in (
                    Service.from_dict(_, __)
                    for _, __ in composefile.items()
                    if _ in service_keys and __['x-bssenv']['type'] == 'service'
                )}
    for service_key in service_keys:
        if service_key not in services.keys():
            raise Exception(f'Service key "{service_key}" not found in given composefile "{path}"')
    # install services to composefiles
    for service in services.values():
        service.image = image_sha
        service.image_sha = image_sha
        service.image_name = image
        service.image_guard_container = image_guard_container_sha
        service.add_label('bssenv.environment.id', env.id())
        service.add_label('bssenv.service.key', service.key)
        service.add_label('bssenv.service.name', service.name)
        service.add_label('bssenv.container.type', 'service')
        service.add_label('bssenv.service.type', service.bssenv['service']['type'])
        if service.is_data_provider_builder:
            service.container_name = None
            del service.composefile_entry['container_name']
        else:
            service.container_name = f'${{BSSENV_NAME}}_{service.container_name or service.key}'
        _escape_url_links(service)
        if service.commands:
            info(f"Install service commands")
            _install_service_commands(service)
        info(f'Install service: {service.key}')
        if SERVICE_TYPES.DAEMON.value in service.types:
            _install_daemon_service(service)
        elif SERVICE_TYPES.COMMAND.value in service.types:
            _install_command_service(service)
        elif SERVICE_TYPES.DATA_PROVIDER.value in service.types:
            _install_data_provider_service(service)
        _create_host_directories_for_service_volumes(service)
        uninstall.remove_uninstalled_services(service.name)
        row = next(_ for _ in progress['_ROWS_'] if _['Service'] == service.key)
        row['Install'] = 'done'
        if use_raw_output() is False:
            screen.update({'progress': progress}, clear_screen=False)
    return services


def _set_dns_mappings_in_composefile(composefile: Dict) -> None:
    dns_mappings = dns.get_added_dns_mappings()
    if len(dns_mappings) > 0:
        debug(f'_set_dns_mappings_in_composefile.dns_mappings: {dns_mappings}')
        for dns_mapping in dns_mappings:
            dns_name, ip_address = dns_mapping.split(':')
            for service in composefile.values():
                extra_hosts = service.get("extra_hosts", [])
                extra_hosts = [_ for _ in extra_hosts
                               if not _.startswith(f'{dns_name}:')]
                extra_hosts.append(dns_mapping)
                service['extra_hosts'] = extra_hosts


def _set_port_mappings_in_composefile(composefile: Dict) -> None:
    port_mappings = ports.get_changed_port_mappings()
    if len(port_mappings.keys()) > 0:
        debug(
            f'_set_port_mappings_in_composefile.port_mappings: '
            f'{port_mappings}')
        for service_key, service in composefile.items():
            if service_key not in port_mappings.keys():
                continue
            service_port_mappings = port_mappings[service_key]
            service_new_port_mappings = dict()
            for port in service.get('ports', []):
                # 9000:9000
                port_host, port_docker = port.split(':')
                service_new_port_mappings[int(port_docker)] = int(port_host)
            service_reapply_ports = dict()
            for label in service.get('labels', []):
                if label.startswith('bssenv.port.'):
                    port_docker = int(label.split('=')[1].rpartition(':')[2])
                    port_names = label.split('=')[0][len('bssenv.port.'):] \
                        .split('.')
                    for port_name in port_names:
                        if port_name in service_port_mappings.keys():
                            service_reapply_ports[port_docker] = \
                                service_port_mappings[port_name]
            for port_docker, port_host in service_reapply_ports.items():
                if port_host is None:
                    if port_docker in service_new_port_mappings.keys():
                        del service_new_port_mappings[port_docker]
                else:
                    service_new_port_mappings[port_docker] = port_host
            service['ports'] = [
                f'{__}:{_}' for _, __ in service_new_port_mappings.items()]
        # TODO: remove port names that are not any more defined??????


def _set_switches_in_composefile(composefile: Dict) -> None:
    switches_dict = switches.get_switch_configurations()
    if len(switches_dict.keys()) > 0:
        debug(f'_set_switches_in_composefile.switches_dict: {switches_dict}')
        for service_key, service in composefile.items():
            if service_key not in switches_dict.keys():
                continue
            service_switches = switches_dict[service_key]
            service_reapply_switches = dict()
            for label in service.get('labels', []):
                if label.startswith('bssenv.switch.'):
                    *_, switch_name, switch_env_name = \
                        label.split('=')[0].split('.')
                    if switch_name in service_switches.keys():
                        service_reapply_switches[switch_env_name] = \
                            service_switches[switch_name]
            service['environment'] = service.get('environment', [])
            for switch_env_name, switch_value in service_reapply_switches \
                    .items():
                service['environment'] = [
                    f'{switch_env_name}={str(switch_value or False).lower()}'
                    if _.startswith(f'{switch_env_name}=') else _
                    for _ in service['environment']]


def _get_images_sha(image: str, dimage: str) -> Tuple[str, str]:
    image = dockerClient.get_image(image)
    dimage = dockerClient.get_image(dimage)
    return image.id, dimage.id


def _create_image_guard_container(image_sha: str) -> str:
    env_id = env.id()
    sha256 = 'sha256:'
    image = dockerClient.get_image(image_sha)
    image_guard_container_name = f'GUARD_{env_id}_{image_sha[len(sha256):]}'
    if not dockerClient.container_exists(image_guard_container_name):
        # overwrite docker-compose labels from image
        # especially: "com.docker.compose.project"
        image_guard_container_sha = \
            dockerClient.create_container(
                image_sha,
                name=image_guard_container_name,
                labels={
                    'bssenv.environment.id': env_id,
                    'bssenv.container.type': 'guard',
                    'bssenv.guarded.image.sha': image_sha,
                    **{_: None for _ in image.labels.keys()
                        if _.startswith('com.docker.compose.')}
                })
    else:
        image_guard_container_sha = \
            dockerClient.get_container(image_guard_container_name).id
    return image_guard_container_sha


def _preprocess_composefile(composefile: Dict) -> None:
    for service in composefile.values():
        service['x-bssenv'] = service.get('x-bssenv', dict())
        bssenv = service['x-bssenv']
        bssenv['image'] = {'guard_container': None, 'name': None, 'sha': None}
        if not bssenv.get('type', None):
            bssenv['type'] = 'service'
        if 'commands' in bssenv.keys():
            for command in bssenv['commands'].values():
                command['uuid'] = None
                command['type'] = command.get('type', COMMAND_TYPES.RUN.value)
                command['allow_multiple'] = command.get(
                    'allow_multiple', False)
        if bssenv.get('command', {}).get('uuid', None):
            bssenv['command']['uuid'] = None
        if 'x-image_guard_container' in service.keys():
            del service['x-image_guard_container']
        if 'x-image_name' in service.keys():
            del service['x-image_name']
        if 'x-image_sha' in service.keys():
            del service['x-image_sha']


def install_services_from_image(image: str, service_keys: Set[Service_key], screen: Screen, progress: Dict[str, Dict]) \
        -> Dict[Service_key, Service]:
    info(f'Install services {service_keys} from image: {image}')
    dimage = entity_image_to_bssenv_descriptor_image(image)
    image_sha, dimage_sha = _get_images_sha(image, dimage)
    image_guard_container_sha = _create_image_guard_container(image_sha)
    composefile_path = _unpack_composefile_from_image_to_tmp(dimage_sha)
    composefile = yaml.file_to_dict(composefile_path)
    _preprocess_composefile(composefile)
    _set_dns_mappings_in_composefile(composefile)
    _set_port_mappings_in_composefile(composefile)
    _set_switches_in_composefile(composefile)
    installed_services = _install_services_from_composefile(
        composefile, composefile_path, service_keys, image, image_sha, image_guard_container_sha, screen, progress)
    add_installed_services(installed_services)
    return installed_services


def _copy_cm_files_from_image_to_host(
        image_sha: str, src_path: Path, dst_path: Path) -> None:
    if dst_path.exists():
        if dst_path.is_file():
            dst_path.unlink()
        elif dst_path.is_dir():
            shutil.rmtree(str(dst_path))
    dst_path.mkdir()
    container = None
    extracted_path = None
    try:
        container = dockerClient.create_container(image_sha, command='true')
        dockerClient.export_container_path(container, src_path, dst_path)
        src_name = src_path.name
        extracted_path = dst_path / src_name
        tmp_uuid = str(uuid.uuid4())
        if extracted_path.is_dir():
            extracted_path = extracted_path.rename(f"{extracted_path}.{tmp_uuid}")
            for file_name in listdir(extracted_path):
                shutil.move(
                    str(extracted_path / file_name),
                    str(dst_path / file_name))
            extracted_path.rmdir()
        elif extracted_path.is_file():
            extracted_path = extracted_path.rename(f"{dst_path}.{tmp_uuid}")
            dst_path.rmdir()
            extracted_path = extracted_path.rename(dst_path)
    finally:
        if container is not None:
            dockerClient.rm_container(container)


def install_config_maps_from_image(
        image_name: str, config_maps: Set[SimpleConfigMap], screen: Screen, progress: Dict[str, Dict]) \
        -> Set[Config_map_key]:
    installed_config_maps: Dict[Config_map_key, InstalledConfigMapsEntry] = dict()
    image = dockerClient.get_image(image_name)
    image_sha = image.id
    for config_map in config_maps:
        info(f'Install config map {config_map.name} from image: {image_name}')
        host_path = paths.ENV_CONFIG_MAPS_DIR / config_map.name
        _copy_cm_files_from_image_to_host(image_sha, Path(config_map.path), host_path)
        installed_cm_entry = InstalledConfigMapsEntry()
        installed_cm_entry.key = config_map.name
        installed_cm_entry.image_name = image_name
        installed_cm_entry.image_sha = image_sha
        installed_cm_entry.type = config_map.cm_tyoe
        installed_config_maps[config_map.name] = installed_cm_entry
        row = next(_ for _ in progress['_ROWS_'] if _['Config map'] == config_map.name)
        row['Install'] = 'done'
        if use_raw_output() is False:
            screen.update({'progress': progress}, clear_screen=False)
    add_installed_config_maps(installed_config_maps)
    return set(installed_config_maps.keys())
