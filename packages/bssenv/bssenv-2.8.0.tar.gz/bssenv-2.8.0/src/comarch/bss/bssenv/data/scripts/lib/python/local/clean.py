# imports from normal python site packages
import sys
from pathlib import Path
import local.install
import local.init
from local.docker import dockerClient
from itertools import repeat, chain
from typing import List
from local.os import exec2
from os.path import expandvars
from local.regex import is_like
from local.entities import Service
from local.logging import debug
from local.paths import ENV_DOCKER_DATA_VOLUME, ENV_DOCKER_CONFIG_VOLUME, \
    ENV_DOCKER_LOGS_VOLUME
import local.os
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


def _clean_path_in_container(
        container_path: str, volumes: List[str]) -> None:
    if not dockerClient.image_exists('bash:latest'):
        dockerClient.pull_image('bash:latest')
    debug(f'Clean path "{container_path}" for volumes: {volumes}')
    result = exec2(
        ['docker', 'run', '--rm',
         *chain.from_iterable(zip(repeat('-v'), volumes)),
         'bash:latest',
         'bash', '-c', f'if [[ -d "{container_path}" ]]; then find "{container_path}" -mindepth 1 -delete; fi'  # noqa: E501
         ])
    if result.returncode != 0:
        raise Exception(
            f'Can\'t clean path in container: \n'
            f'{result.stdout}\n'
            f'{result.stderr}')
    debug(f'clean stdout: {result.stdout}')


def _get_service_volumes(service: Service) -> List[str]:
    return list(
        f'{Path(expandvars(_)).resolve()}:{__}' for _, __ in
        (_.split(':')[0:2] for _ in service.composefile_entry.get(
            'volumes', [])
         if isinstance(_, str)
         and is_like(_, '^[^:]+:[^:]+(:[^:]+)?$')))


def data(service_name: str) -> None:
    for service in local.install.get_installed_services().values():
        if service.name == service_name and service.data_path is not None:
            container_path = service.data_path
            volumes = _get_service_volumes(service)
            if len(volumes) > 0:
                _clean_path_in_container(container_path, volumes)


def conf(service_name: str) -> None:
    for service in local.install.get_installed_services().values():
        if service.name == service_name and service.conf_path is not None:
            container_path = service.conf_path
            volumes = _get_service_volumes(service)
            if len(volumes) > 0:
                _clean_path_in_container(container_path, volumes)


def logs(service_name: str) -> None:
    for service in local.install.get_installed_services().values():
        if service.name == service_name and service.logs_path is not None:
            container_path = service.logs_path
            volumes = _get_service_volumes(service)
            if len(volumes) > 0:
                _clean_path_in_container(container_path, volumes)


def init(service_name: str) -> None:
    for service in local.install.get_installed_services().values():
        if service.name == service_name \
                and local.init.is_initialized(service.key):
            local.init.remove_initialized(service.key)


def data_volume() -> None:
    container_path = '/clean/data'
    host_path = str(ENV_DOCKER_DATA_VOLUME)
    _clean_path_in_container(container_path, [f'{host_path}:{container_path}'])


def conf_volume() -> None:
    container_path = '/clean/conf'
    host_path = str(ENV_DOCKER_CONFIG_VOLUME)
    _clean_path_in_container(container_path, [f'{host_path}:{container_path}'])


def logs_volume() -> None:
    container_path = '/clean/logs'
    host_path = str(ENV_DOCKER_LOGS_VOLUME)
    _clean_path_in_container(container_path, [f'{host_path}:{container_path}'])
