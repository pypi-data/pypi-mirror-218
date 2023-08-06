# imports from normal python site packages
import sys
from pathlib import Path
from typing import Set
import threading
import local.paths
import local.os
import local.install
import local.services
import local.ports
import local.switches
import local.commands
from local.docker import dockerClient
from local.logging import debug, info
from local.entities import SERVICE_TYPES, COMPOSEFILE_TYPES, Service
from local.cache import FileCacheEntry, CacheTransformer, Cache
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / 'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


lock_uninstalled_services_file = threading.RLock()
lock_uninstalled_config_maps_file = threading.RLock()
UNINSTALLED_SERVICES_FILE_CACHE = Cache()
UNINSTALLED_CONFIG_MAPS_FILE_CACHE = Cache()
ENV_UNINSTALLED_SERVICES_FILE = local.paths.ENV_UNINSTALLED_SERVICES_FILE
ENV_UNINSTALLED_CONFIG_MAPS_FILE = local.paths.ENV_UNINSTALLED_CONFIG_MAPS_FILE
Entity_key = str
Config_map_key = str
Config_map_name = str
Service_name = str


class UninstalledConfigMapsCacheTransformer(CacheTransformer):

    def transform(self) -> Set[Config_map_key]:
        if self.value is not None:
            self.value = set([_.strip() for _ in self.value.splitlines() if len(_.strip()) > 0])
        else:
            self.value = set()
        return self.value


class UninstalledConfigMapsFileCacheEntry(UninstalledConfigMapsCacheTransformer, FileCacheEntry):
    pass


def get_uninstalled_config_maps() -> Set[Config_map_key]:
    with lock_uninstalled_config_maps_file:
        if not UNINSTALLED_CONFIG_MAPS_FILE_CACHE.exists(ENV_UNINSTALLED_CONFIG_MAPS_FILE):
            UNINSTALLED_CONFIG_MAPS_FILE_CACHE.add(
                UninstalledConfigMapsFileCacheEntry(ENV_UNINSTALLED_CONFIG_MAPS_FILE))
        return UNINSTALLED_CONFIG_MAPS_FILE_CACHE.get(ENV_UNINSTALLED_CONFIG_MAPS_FILE)


def is_uninstalled_config_map(config_map_key: str) -> bool:
    return config_map_key in get_uninstalled_config_maps()


def set_uninstalled_config_maps(*config_maps_keys: str) -> None:
    with lock_uninstalled_config_maps_file:
        ENV_UNINSTALLED_CONFIG_MAPS_FILE.write_text("\n".join(config_maps_keys) + "\n")


def add_uninstalled_config_maps(*config_maps_keys: str) -> None:
    if len(config_maps_keys) > 0:
        all_config_maps_keys = get_uninstalled_config_maps().copy()  # do not modify cached set directly!
        all_config_maps_keys.update(config_maps_keys)
        set_uninstalled_config_maps(*all_config_maps_keys)


def remove_uninstalled_config_maps(*config_maps_keys: str) -> None:
    if len(config_maps_keys) < 1:
        with lock_uninstalled_config_maps_file:
            ENV_UNINSTALLED_CONFIG_MAPS_FILE.write_text('')
    else:
        config_maps_keys = set(config_maps_keys)
        all_config_maps_keys = get_uninstalled_config_maps().copy()  # do not modify cached set directly!
        if not config_maps_keys.isdisjoint(all_config_maps_keys):
            all_config_maps_keys -= config_maps_keys
            set_uninstalled_config_maps(*all_config_maps_keys)


def uninstall_config_map(config_map_key: str, intentional: bool = False) -> None:
    if config_map_key in local.install.get_installed_config_maps_keys():
        debug('Remove config map from installed config maps registry')
        local.install.remove_installed_config_map(config_map_key)
        debug('Remove config map files from filesystem')
        host_path = local.paths.ENV_CONFIG_MAPS_DIR / config_map_key
        local.os.remove_path(host_path)
        if intentional:
            # user has run manually command "uninstall". So he wants this
            # config map to be uninstalled untill it is manually installed
            # again by him
            debug('Add config map to uninstalled config maps regaistry')
            add_uninstalled_config_maps(config_map_key)


class UninstalledServicesCacheTransformer(CacheTransformer):

    def transform(self) -> Set[Service_name]:
        if self.value is not None:
            self.value = set([_.strip() for _ in self.value.splitlines() if len(_.strip()) > 0])
        else:
            self.value = set()
        return self.value


class UninstalledServicesFileCacheEntry(UninstalledServicesCacheTransformer, FileCacheEntry):
    pass


def get_uninstalled_services() -> Set[Service_name]:
    with lock_uninstalled_services_file:
        if not UNINSTALLED_SERVICES_FILE_CACHE.exists(ENV_UNINSTALLED_SERVICES_FILE):
            UNINSTALLED_SERVICES_FILE_CACHE.add(UninstalledServicesFileCacheEntry(ENV_UNINSTALLED_SERVICES_FILE))
        return UNINSTALLED_SERVICES_FILE_CACHE.get(ENV_UNINSTALLED_SERVICES_FILE)


def is_uninstalled_service(service_name: str) -> bool:
    return service_name in get_uninstalled_services()


def set_uninstalled_services(*service_names: str) -> None:
    with lock_uninstalled_services_file:
        ENV_UNINSTALLED_SERVICES_FILE.write_text("\n".join(service_names) + "\n")


def add_uninstalled_services(*service_names: str) -> None:
    if len(service_names) > 0:
        all_services = get_uninstalled_services().copy()  # do not modify cached set directly!
        all_services.update(service_names)
        set_uninstalled_services(*all_services)


def remove_uninstalled_services(*service_names: str) -> None:
    if len(service_names) < 1:
        with lock_uninstalled_services_file:
            ENV_UNINSTALLED_SERVICES_FILE.write_text('')
    else:
        service_names = set(service_names)
        all_services = get_uninstalled_services().copy()  # do not modify cached set directly!
        if not service_names.isdisjoint(all_services):
            all_services -= service_names
            set_uninstalled_services(*all_services)


def _remove_service_from_composefile(
        service: Service, composefile_type: str,
        composefile_name: str) -> None:
    debug(f'Remove service "{service.key}" from composefile "{composefile_name}"')
    composefile = local.composefile.get_composefile(composefile_name, composefile_type)
    if composefile is not None:
        if service.key in composefile.get('services', {}):
            del (composefile['services'][service.key])
        if composefile_type == COMPOSEFILE_TYPES.DAEMON.value or len(composefile.get('services', {}).keys()) > 0:
            local.composefile.set_composefile(composefile, composefile_name, composefile_type)
        else:
            debug('Composefile with no services inside. Remove it')
            composefile_path = local.composefile.get_path_for_composefile(composefile_name, composefile_type)
            composefile_path.unlink()


def _uninstall_daemon_service(service: Service) -> None:
    composefile_name = 'daemons.yml'
    composefile_type = COMPOSEFILE_TYPES.DAEMON.value
    _remove_service_from_composefile(service, composefile_type, composefile_name)


def _uninstall_command_service(service: Service) -> None:
    composefile_name = f'{service.name}.yml'
    composefile_type = COMPOSEFILE_TYPES.COMMAND.value
    _remove_service_from_composefile(service, composefile_type, composefile_name)
    local.commands.remove_command_from_command_registry(service)
    if service.command_shell_name:
        # remove command shell script
        local.commands.remove_shell_script_from_command_registry(service, service.command_shell_name)
        if service.autocompletion:
            # remove command shell script autocompletion
            local.commands.remove_autocompletion_from_command_registry(service, service.command_shell_name)


def _uninstall_data_provider_service(service: Service) -> None:
    composefile_name = f'{service.name}.yml'
    composefile_type = COMPOSEFILE_TYPES.DATA_PROVIDER.value
    _remove_service_from_composefile(service, composefile_type, composefile_name)


def _uninstall_service_command(service: Service, command_key: str) -> None:
    local.commands.remove_command_from_command_registry(service, command_key)
    command = service.commands[command_key]
    shell_script_name = command.get('generate_script', None)
    if shell_script_name:
        # remove command shell script
        local.commands.remove_shell_script_from_command_registry(service, shell_script_name, command_key)
        if command.get('autocompletion', None):
            # remove command shell script autocompletion
            local.commands.remove_autocompletion_from_command_registry(service, shell_script_name, command_key)
    # remove command lock file
    command_registry = local.commands.get_command_registry()
    commands = command_registry.get('commands', {})
    if command_key not in commands.keys():
        lock_file = local.paths.ENV_LOCKS_DIR / f'{service.key}.{command_key}.lock'
        if lock_file.exists():
            lock_file.unlink()


def uninstall_service(
        service_name: str, intentional: bool = False) -> None:
    # INFO: nie dodawaj tutaj usuwania wolumenów serwisu. Takie usuwanie
    # tylko poprzez jawną komendę "clean" wywołaną manualnie przez usera
    remove_image_guard_containers = set()
    skip_image_guard_containers = set()
    for service in list(local.install.get_installed_services().values()):
        if service.name == service_name:
            info(f'Uninstall service: {service.key}')
            if not service.is_data_provider_builder:
                debug('Stop service')
                local.services.stop(service.key, wait=True)
            debug('Remove service from installed services registry')
            local.install.remove_installed_service(service.key)
            if service.commands:
                for command_key in service.commands.keys():
                    _uninstall_service_command(service, command_key)
            if intentional:
                debug('Remove service from changed port mappings')
                local.ports.remove_changed_port_mapping(service.key)
                debug('Remove service from switches configurations')
                local.switches.remove_switch_configuration(service.key)
            debug('Remove service container')
            if service.container_name is not None:
                dockerClient.rm_container(service.container_name)
            if service.main_type == SERVICE_TYPES.DAEMON.value:
                _uninstall_daemon_service(service)
            elif service.main_type == SERVICE_TYPES.COMMAND.value:
                _uninstall_command_service(service)
            elif service.main_type == SERVICE_TYPES.DATA_PROVIDER.value:
                _uninstall_data_provider_service(service)
            remove_image_guard_containers |= {service.image_guard_container}
        else:
            skip_image_guard_containers |= {service.image_guard_container}
    # remove unused guard containers
    remove_image_guard_containers -= skip_image_guard_containers
    for container in remove_image_guard_containers:
        if dockerClient.container_exists(container):
            dockerClient.rm_container(container)
    # INFO: do not remove images and bssenv composefiles images
    # because of layer caching. Leave this decision to user and let him
    # do images pruning manually
    if intentional:
        # user has run manually command "uninstall". So he wants this
        # service to be uninstalled untill it is manually installed again
        # by him
        debug('Add service to uninstalled services registry')
        add_uninstalled_services(service_name)
