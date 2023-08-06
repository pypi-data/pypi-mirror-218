# imports from normal python site packages
import sys
import os
import shlex
import threading
import local.paths
import local.services
from local.docker import dockerClient
from pathlib import Path
from typing import Set
from local.entities import INIT_TYPES, Service
from local.paths import ENV_MAIN_LOG_FILE
from local.os import fexec
from local.cache import Cache, CacheTransformer, FileCacheEntry
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


lock = threading.RLock()
Cache = Cache()
ENV_DIR = local.paths.ENV_DIR
ENV_INITIALIZED_SERVICES_FILE = local.paths.ENV_INITIALIZED_SERVICES_FILE
ENV_TMP_DIR = local.paths.ENV_TMP_DIR
Service_key = str


class InitializedServicesCacheTransformer(CacheTransformer):

    def transform(self) -> Set[Service_key]:
        if self.value is not None:
            self.value = set(
                [_.strip() for _ in self.value.splitlines()
                 if len(_.strip()) > 0])
        else:
            self.value = set()
        return self.value


class InitializedServicesFileCacheEntry(
        InitializedServicesCacheTransformer, FileCacheEntry):
    pass


def get_initialized() -> Set[Service_key]:
    with lock:
        if not Cache.exists(
                ENV_INITIALIZED_SERVICES_FILE):
            Cache.add(
                InitializedServicesFileCacheEntry(
                    ENV_INITIALIZED_SERVICES_FILE))
        return Cache.get(ENV_INITIALIZED_SERVICES_FILE)


def set_initialized(service_key: str) -> None:
    with lock:
        initialized = get_initialized() | set([service_key])
        ENV_INITIALIZED_SERVICES_FILE.write_text('\n'.join(initialized) + '\n')


def remove_initialized(service_key: str = None) -> None:
    with lock:
        if service_key is None:
            # remove all
            ENV_INITIALIZED_SERVICES_FILE.write_text('')
        else:
            # remove one
            initialized = get_initialized() - set([service_key])
            ENV_INITIALIZED_SERVICES_FILE.write_text(
                '\n'.join(initialized) + '\n')


def is_initialized(service_key: str) -> bool:
    return service_key in get_initialized()


def initialize(
        service: Service,
        keep_running_service: bool = False,
        force: bool = False) -> None:
    if service.has_init_command \
            and (
                force
                or service.init_command_type == INIT_TYPES.ALWAYS.value
                or (
                    service.init_command_type == INIT_TYPES.ONETIME.value
                    and not is_initialized(service.key))):
        composefile_path = \
            local.composefile.get_path_for_service_name_composefile(
                service.name, service.main_type)
        if composefile_path.exists():
            was_running_service = False
            if dockerClient.is_running_container(service.container_name):
                was_running_service = True
                local.services.stop(service.key, wait=True)
            fexec(
                ['docker-compose', 'run', '--rm', service.key,
                 *shlex.split(service.init_command)],
                env={
                    **os.environ,
                    'COMPOSE_FILE': str(composefile_path)}) \
                >> ENV_MAIN_LOG_FILE
            set_initialized(service.key)
            if keep_running_service and was_running_service:
                local.services.start(service.key)
        else:
            raise Exception(f'Composefile for service key "{service.key}" '
                            f'and type "{service.main_type}" not found')
