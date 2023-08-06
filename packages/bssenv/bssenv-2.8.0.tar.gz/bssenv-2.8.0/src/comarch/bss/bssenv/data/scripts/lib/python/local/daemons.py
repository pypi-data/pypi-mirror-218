# imports from normal python site packages
import sys
import os
from pathlib import Path
import local.composefile
import local.services
import local.install
import local.docker
from local.logging import info
from local.os import fexec, run
from local.paths import ENV_MAIN_LOG_FILE
from local.entities import COMPOSEFILE_TYPES
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


DAEMON_COMPOSEFILE_PATH = \
    local.composefile.get_path_for_composefile(
        composefile_type=COMPOSEFILE_TYPES.DAEMON.value)
Service_key = str


# def create_containers(recreate: bool = False) -> None:
def create_containers(recreate: bool = True) -> None:
    fexec([
            'docker-compose', 'up',
            *([] if recreate else ['--no-recreate']),
            # '--quiet-pull',  ???
            # '--remove-orphans',  ???
            '--no-start'],
          env={
                **os.environ,
                # 'COMPOSE_IGNORE_ORPHANS': 'false',
                'COMPOSE_FILE': str(DAEMON_COMPOSEFILE_PATH)}) \
        >> ENV_MAIN_LOG_FILE


def up(*service_keys: str) -> None:
    service_keys = set(service_keys)
    if len(service_keys) < 1:
        # up all daemons
        service_keys = set(_.key for _ in local.install.get_installed_services().values() if _.is_daemon)
    for service_key in service_keys:
        if not local.install.is_installed_service(service_key):
            raise Exception(f'Service "{service_key}" is not installed"')
    services = [
        _ for _ in local.install.get_installed_services().values()
        if _.is_daemon and _.key in service_keys]
    service_keys = [_.key for _ in services]
    if len(service_keys) > 0:
        info(f'Start up daemons: {service_keys}')
        if os.environ.get('BSSENV_STDOUT_MODE', 'false') == 'true':
            run(
                ['docker-compose', 'up', '-d', *service_keys],
                env={
                    **os.environ,
                    'COMPOSE_FILE': str(DAEMON_COMPOSEFILE_PATH)})
        else:
            fexec(
                ['docker-compose', 'up', '-d', *service_keys],
                env={
                    **os.environ,
                    'COMPOSE_FILE': str(DAEMON_COMPOSEFILE_PATH)}) \
                >> ENV_MAIN_LOG_FILE
