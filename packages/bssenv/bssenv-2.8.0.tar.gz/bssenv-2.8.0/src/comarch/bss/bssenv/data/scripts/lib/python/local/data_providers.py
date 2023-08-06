# imports from normal python site packages
import sys
import os
from pathlib import Path
import local.composefile
import local.services
import local.install
from local.os import fexec, run
from local.logging import debug, info
from local.entities import SERVICE_TYPES
from local.paths import ENV_MAIN_LOG_FILE
import comarch.bss.bssenv as BSSENV_PKG

# TODO: wydaje mi sie ze manipulacje na sys.path powinny byc tylko na poziomie skryptow z bin. W libach juz nie trzeba
# bo jak jest ladowany lib to wlasciwa sciezka jest juz w pathie
# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


def restore(
        service_key: str,
        preserve_ownership=False) -> None:
    if not local.install.is_installed_service(service_key):
        raise Exception(f'Service "{service_key}" is not installed"')
    debug(f'restore.service_key: {service_key}')
    service = local.services.get_service(service_key)
    if SERVICE_TYPES.DATA_PROVIDER_RESTORE.value in service.types:
        info(f'Restore data from data provider: {service_key}')
        composefile_path = \
            local.composefile.get_path_for_service_name_composefile(
                service.name, service.main_type)
        debug(f'restore.composefile_path: {composefile_path}')
        if os.environ.get('BSSENV_STDOUT_MODE', 'false') == 'true':
            run(
                ['docker-compose', 'run', '--rm',
                 '-e', f'PRESERVE_OWNERSHIP={str(preserve_ownership).lower()}',
                 '--name', service.container_name, service_key],
                env={**os.environ, 'COMPOSE_FILE': str(composefile_path)})
        else:
            fexec(
                ['docker-compose', 'run', '--rm',
                 '-e', f'PRESERVE_OWNERSHIP={str(preserve_ownership).lower()}',
                 '--name', service.container_name, service_key],
                env={**os.environ, 'COMPOSE_FILE': str(composefile_path)}) \
                >> ENV_MAIN_LOG_FILE
    else:
        raise Exception(f'Service key "{service_key}" is not of type'
                        f'"{SERVICE_TYPES.DATA_PROVIDER_RESTORE.value}"')


def build(service_key: str) -> None:
    if not local.install.is_installed_service(service_key):
        raise Exception(f'Service "{service_key}" is not installed"')
    service = local.services.get_service(service_key)
    if SERVICE_TYPES.DATA_PROVIDER_BUILD.value in service.types:
        info(f'Build data container by data provider: {service_key}')
        composefile_path = \
            local.composefile.get_path_for_service_name_composefile(
                service.name, service.main_type)
        if os.environ.get('BSSENV_STDOUT_MODE', 'false') == 'true':
            run(
                ['docker-compose', 'build', '--pull', service_key],
                env={**os.environ, 'COMPOSE_FILE': str(composefile_path)})
        else:
            fexec(
                ['docker-compose', 'build', '--pull', service_key],
                env={**os.environ, 'COMPOSE_FILE': str(composefile_path)}) \
                >> ENV_MAIN_LOG_FILE
    else:
        raise Exception(f'Service key "{service_key}" is not of type'
                        f'"{SERVICE_TYPES.DATA_PROVIDER_BUILD.value}"')


def compress(service_key: str) -> None:
    if not local.install.is_installed_service(service_key):
        raise Exception(f'Service "{service_key}" is not installed"')
    service = local.services.get_service(service_key)
    if SERVICE_TYPES.DATA_PROVIDER_COMPRESS.value in service.types:
        info(f'Compress data by data provider: {service_key}')
        composefile_path = \
            local.composefile.get_path_for_service_name_composefile(
                service.name, service.main_type)
        if os.environ.get('BSSENV_STDOUT_MODE', 'false') == 'true':
            run(
                ['docker-compose', 'run', '--rm',
                 '--name', service.container_name, service_key],
                env={**os.environ, 'COMPOSE_FILE': str(composefile_path)})
        else:
            fexec(
                ['docker-compose', 'run', '--rm',
                 '--name', service.container_name, service_key],
                env={**os.environ, 'COMPOSE_FILE': str(composefile_path)}) \
                >> ENV_MAIN_LOG_FILE
    else:
        raise Exception(f'Service key "{service_key}" is not of type'
                        f'"{SERVICE_TYPES.DATA_PROVIDER_COMPRESS.value}"')
