# imports from normal python site packages
import sys
from pathlib import Path
from typing import Dict
import copy
import threading
import local.paths
import local.yaml
import local.os
from local.entities import SERVICE_TYPES, COMPOSEFILE_TYPES, Service
from local.cache import YamlFileCacheEntry, Cache
from local.logging import debug
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


lock = threading.RLock()
Cache = Cache()
ENV_COMPOSEFILES_DIR = local.paths.ENV_COMPOSEFILES_DIR
ENV_MAIN_COMPOSEFILE_FILE = local.paths.ENV_MAIN_COMPOSEFILE_FILE
ENV_COMPOSEFILES_COMMANDS_DIR = local.paths.ENV_COMPOSEFILES_COMMANDS_DIR
ENV_COMPOSEFILES_DATA_PROVIDERS_DIR = \
    local.paths.ENV_COMPOSEFILES_DATA_PROVIDERS_DIR
ENV_TEMPLATE_COMPOSEFILE_FILE = local.paths.ENV_TEMPLATE_COMPOSEFILE_FILE


def get_composefile_name_for_service(service: Service):
    return 'daemons.yml' \
        if service.main_type == SERVICE_TYPES.DAEMON.value \
        else f'{service.name}.yml'


def get_composefile_name_for_service_type(
        service_name: str, service_type: str):
    return 'daemons.yml' \
        if service_type == SERVICE_TYPES.DAEMON.value \
        else f'{service_name}.yml'


def get_path_for_composefile(
        composefile_name: str = None,
        composefile_type: str = None) -> Path:
    composefile_path = None
    if composefile_name is None or composefile_name == 'daemons.yml':
        if composefile_type is not None \
                and composefile_type != COMPOSEFILE_TYPES.DAEMON.value:
            raise Exception(f'If composefile name is None then '
                            f'type should be None or '
                            f'{COMPOSEFILE_TYPES.DAEMON.value}')
        composefile_path = ENV_MAIN_COMPOSEFILE_FILE
    elif composefile_type in [
            COMPOSEFILE_TYPES.COMMAND.value,
            COMPOSEFILE_TYPES.DATA_PROVIDER.value]:
        composefile_path = (ENV_COMPOSEFILES_COMMANDS_DIR
                            if
                            composefile_type == COMPOSEFILE_TYPES.COMMAND.value
                            else ENV_COMPOSEFILES_DATA_PROVIDERS_DIR) / \
                            composefile_name
    else:
        raise Exception(f'Wrong parameters provided: '
                        f'{composefile_name}, {composefile_type}')
    return composefile_path


def get_path_for_service_name_composefile(
        service_name: str, service_type: str) -> Path:
    composefile_name = get_composefile_name_for_service_type(
            service_name, service_type)
    return get_path_for_composefile(composefile_name, service_type)


def get_template() -> Dict:
    with lock:
        if not Cache.exists(ENV_TEMPLATE_COMPOSEFILE_FILE):
            Cache.add(YamlFileCacheEntry(ENV_TEMPLATE_COMPOSEFILE_FILE))
        return copy.deepcopy(Cache.get(ENV_TEMPLATE_COMPOSEFILE_FILE))


def exists(composefile_name: str, composefile_type: str) -> bool:
    return get_path_for_composefile(
        composefile_name, composefile_type).exists()


def set_composefile(
        composefile: Dict,
        composefile_name: str,
        composefile_type: str) -> None:
    with lock:
        composefile_path = get_path_for_composefile(
            composefile_name, composefile_type)
        local.yaml.dict_to_file(composefile, composefile_path)


def get_composefile(composefile_name: str, composefile_type: str) -> Dict:
    composefile_path = get_path_for_composefile(
        composefile_name, composefile_type)
    with lock:
        debug(f'get_composefile: '
              f'{composefile_name}, {composefile_type}, {composefile_path}')
        if not Cache.exists(composefile_path):
            debug('add composefile to cache')
            Cache.add(YamlFileCacheEntry(composefile_path))
        return Cache.get(composefile_path)


def get_service_name_composefile(
        service_name: str, service_type: str) -> Dict:
    with lock:
        composefile_path = get_path_for_service_name_composefile(
            service_name, service_type)
        if not Cache.exists(composefile_path):
            Cache.add(YamlFileCacheEntry(composefile_path))
        return Cache.get(composefile_path)


def update_service_composefile(service: Service) -> None:
    composefile_name = get_composefile_name_for_service(service)
    composefile = get_service_name_composefile(service.name, service.main_type)
    composefile['services'][service.key] = service.composefile_entry
    set_composefile(
            composefile,
            composefile_name,
            service.main_type)
