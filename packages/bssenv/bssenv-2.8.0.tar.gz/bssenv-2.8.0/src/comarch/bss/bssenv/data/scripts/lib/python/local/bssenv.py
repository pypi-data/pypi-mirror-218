# imports from normal python site packages
import sys
import os
import uuid
import threading
from os import PathLike
from pathlib import Path
from typing import Dict
from .logging import info
from .entities import SNAPSHOT_TYPES
from .itertools import each
from .os import exec2
from .cache import Cache, CacheTransformer, FileCacheEntry
from .docker import dockerClient
from .const import BSSENV_DOCKER_NETWORK_MTU
from .snapshots import snapshot_exists, get_snapshot_metadata
from .os import create_dir, remove_path, copy_path, get_uid_gid
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PKG_DIR = Path(BSSENV_PKG.__file__).resolve().parent
BSSENV_PKG_PYT_SITE_PKGS = BSSENV_PKG_DIR / 'data' / 'python_site_packages'
sys.path = [str(BSSENV_PKG_PYT_SITE_PKGS)] + sys.path

# import from custom site packages
import portalocker


lock = threading.RLock()
Cache = Cache()
BSSENV_PKG_DATA_DIR = BSSENV_PKG_DIR / 'data'
BSSENV_PKG_CONFIG_DIR = BSSENV_PKG_DATA_DIR / 'config'
BSSENV_ENVIRONMENTS_FILE = \
    Path((BSSENV_PKG_CONFIG_DIR / 'bssenv_environments').read_text().strip())
BSSENV_ENVIRONMENTS_LOCK_FILE = f'{BSSENV_ENVIRONMENTS_FILE}.lock'

INSTALL_TYPE = \
    (BSSENV_PKG_CONFIG_DIR / 'install_type').read_text().strip()
VERSION = \
    (BSSENV_PKG_CONFIG_DIR / 'bssenv_version').read_text().strip()


class EnvironmentsFileCacheTransformer(CacheTransformer):

    def transform(self) -> Dict[str, str]:
        if self.value is not None:
            self.value = {_: Path(__) for _, __ in
                          (_.split('|', 1) for _ in self.value.splitlines()
                           if '|' in _ and not _.startswith('#'))}
        return self.value


class EnvironmentsFileCacheEntry(
        EnvironmentsFileCacheTransformer, FileCacheEntry):
    pass


def environments() -> Dict[str, str]:
    with lock:
        if not Cache.exists(
                BSSENV_ENVIRONMENTS_FILE):
            Cache.add(
                EnvironmentsFileCacheEntry(
                    BSSENV_ENVIRONMENTS_FILE))
        return Cache.get(BSSENV_ENVIRONMENTS_FILE)


def get_environment_path(env_name: str) -> Path:
    if env_name not in environments().keys():
        raise Exception(f'Environment with name "{env_name}" not found')
    return environments()[env_name]


def environment_exists(env_name: str) -> bool:
    return env_name in environments().keys()


def set_environment_to_environments_file(
        env_name: str, path: PathLike) -> None:
    with portalocker.Lock(
            BSSENV_ENVIRONMENTS_LOCK_FILE, 'a', timeout=10):
        envs = environments()
        envs[env_name] = path
        BSSENV_ENVIRONMENTS_FILE.write_text(
            '\n'.join(f'{_}|{__}' for _, __ in envs.items()))


def rm_environment_from_environments_file(env_name: str) -> None:
    with portalocker.Lock(
            BSSENV_ENVIRONMENTS_LOCK_FILE, 'a', timeout=10):
        envs = environments()
        del envs[env_name]
        BSSENV_ENVIRONMENTS_FILE.write_text(
            '\n'.join(f'{_}|{__}' for _, __ in envs.items()))


def create_environment_docker_network(env_name: str) -> None:
    network_name = f'{env_name}_network'
    if dockerClient.network_exists(network_name):
        info(f'Network with name "{network_name}" already exists. '
             f'Will use this network\n'
             f'Please check what endpoints are '
             f'connected to this network\n')
    else:
        mtu = BSSENV_DOCKER_NETWORK_MTU
        dockerClient.create_network(
            network_name, driver="bridge", internal=False,
            attachable=False, ingress=False, scope='local',
            options={'com.docker.network.driver.mtu': str(mtu)})


def create_environment(env_name: str, path: PathLike) -> None:
    if environment_exists(env_name):
        raise Exception(f'Environment with name "{env_name}" already exists')
    env_path = Path(path) / env_name
    if env_path.exists():
        raise Exception(f'Environment directory with name "{env_name}" already exists')
    # create structure
    each([
        env_path,
        env_path / 'docker/volumes/bss_config',
        env_path / 'docker/volumes/bss_data',
        env_path / 'docker/volumes/bss_logs',
        env_path / '.venv',
        env_path / '.venv/var',
        env_path / '.venv/var/locks',
        env_path / '.venv/var/command_registry',
        env_path / 'logs',
        env_path / 'PML',
        env_path / 'config_maps',
        env_path / '.tmp'], create_dir)
    each([
        env_path / '.env',
        env_path / '.bssenv',
        env_path / '.venv/var/installed',
        env_path / '.venv/var/uninstalled',
        env_path / '.venv/var/initialized',
        env_path / '.venv/var/dns_mappings',
        env_path / '.venv/var/port_mappings',
        env_path / '.venv/var/switches'], Path.touch)
    (env_path / '.bssenv').write_text(str(uuid.uuid1()))
    # copy files
    each([
        (BSSENV_PKG_DATA_DIR / 'config', env_path / 'config'),
        (BSSENV_PKG_DATA_DIR / 'composefiles',
         env_path / 'docker/composefiles'),
        (BSSENV_PKG_DATA_DIR / 'scripts/autocompletion',
         env_path / '.venv/autocompletion'),
        (BSSENV_PKG_DATA_DIR / 'scripts/bin', env_path / '.venv/bin'),
        (BSSENV_PKG_DATA_DIR / 'scripts/bin2', env_path / '.venv/bin2'),
        (BSSENV_PKG_DATA_DIR / 'scripts/lib', env_path / '.venv/lib'),
        (BSSENV_PKG_DATA_DIR / 'templates', env_path / '.venv/templates'),
        (env_path / '.venv/templates/composefiles/template.yml',
         env_path / 'docker/composefiles/daemons.yml')],
         copy_path, expand='args')
    # create network
    create_environment_docker_network(env_name)
    # register environment
    set_environment_to_environments_file(env_name, env_path)


def create_environment_from_snapshot(
        env_name: str, snapshot_name: str, path: PathLike,
        remote: bool = False) -> None:
    if environment_exists(env_name):
        raise Exception(f'Environment with name "{env_name}" already exists')
    env_path = Path(path) / env_name
    if env_path.exists():
        raise Exception(
            f'Environment directory with name "{env_name}" already exists')
    if not snapshot_exists(snapshot_name, remote):
        raise Exception(
            f'Environment snapshot "{snapshot_name}" not found')
    snapshot_metadata = get_snapshot_metadata(
        snapshot_name, remote)
    if snapshot_metadata.type != SNAPSHOT_TYPES.ENVIRONMENT.value:
        raise Exception(
            f'Wrong snapshot type. Should be '
            f'"{SNAPSHOT_TYPES.ENVIRONMENT.value}"')
    env_image = \
        next((_ for _ in snapshot_metadata.images if '/environment:' in _))
    if remote:
        dockerClient.pull_image(env_image)
    create_dir(env_path)
    # restore environment files from data container
    result = exec2(
        ['docker', 'run', '--rm', '-v', f'{env_path}:/restore',
         '-e', f'PRESERVE_OWNERSHIP=true', env_image, 'restore'])
    if result.returncode != 0:
        raise Exception(f'Snapshot restore error: \n'
                        f'{result.stdout}\n'
                        f'{result.stderr}')
    # change owner for environment files other than docker volumes
    # and for docker volume files give exact permissions as owner to anybody
    uid, gid = get_uid_gid()
    if not dockerClient.image_exists('bash:latest'):
        dockerClient.pull_image('bash:latest')
    result = exec2(
        ['docker', 'run', '--rm',
         '-v', f'{env_path}:/env',
         '-v', f'{env_path}/.venv/bin2/setOwnerAndPrivilegesForEnvFiles:/setOwnerAndPrivilegesForEnvFiles',  # noqa: E501
         '--entrypoint=/setOwnerAndPrivilegesForEnvFiles',
         'bash:latest', str(uid), str(gid)])
    if result.returncode != 0:
        raise Exception(
            f'Set owner and privileges for environment files error: \n'
            f'{result.stdout}\n'
            f'{result.stderr}')
    # change environment id
    (env_path / '.bssenv').write_text(str(uuid.uuid1()))
    # create environment network
    create_environment_docker_network(env_name)
    # register environment
    set_environment_to_environments_file(env_name, env_path)
    # update snapshot images
    UPDATE_SNAPSHOT_IMAGES_PATH = env_path / '.venv/bin2/updateSnapshotImages'
    result = exec2(
        [str(UPDATE_SNAPSHOT_IMAGES_PATH), snapshot_name, str(remote)])
    if result.returncode != 0:
        raise Exception(f'Update snapshot images error: \n'
                        f'{result.stdout}\n'
                        f'{result.stderr}')
    # create guard containers
    # TODO: tutaj chyba brakuje aktywacji przed odpaleniem skryptu i w efekcie
    # powstaja guard containers o nazwach:
    # GUARD_None_9a6fb98680f3c7898a5d905a0a99480c479ed1bed6e5ac98d505e53884baac43
    # gdzie None to env_id
    CREATE_GUARD_CONTAINERS_PATH = \
        env_path / '.venv/bin2/createGuardContainers'
    if CREATE_GUARD_CONTAINERS_PATH.exists():
        result = exec2([str(CREATE_GUARD_CONTAINERS_PATH)])
        if result.returncode != 0:
            raise Exception(f'Create guard containers error: \n'
                            f'{result.stdout}\n'
                            f'{result.stderr}')
    UPDATE_COMPOSEFILES_PATH = \
        env_path / '.venv/bin2/updateComposeFilesAfterCreateFromSnap'
    if UPDATE_COMPOSEFILES_PATH.exists():
        result = exec2([str(UPDATE_COMPOSEFILES_PATH)])
        if result.returncode != 0:
            raise Exception(f'Update composefiles error: \n'
                            f'{result.stdout}\n'
                            f'{result.stderr}')
    # create daemon containers
    DAEMON_COMPOSEFILE_PATH = env_path / 'docker/composefiles/daemons.yml'
    result = exec2(
        [f'source "{env_path / ".venv/bin/activate"}"; '
         f'docker-compose pull --ignore-pull-failures -q; '
         f'docker-compose up --no-start'],
        shell=True, executable='/bin/bash',
        env={**os.environ,
             'COMPOSE_FILE': str(DAEMON_COMPOSEFILE_PATH)})
    if result.returncode != 0:
        raise Exception(f'Containers create error: \n'
                        f'{result.stdout}\n'
                        f'{result.stderr}')


def rm_environment(env_name: str) -> None:
    # remove all environment containers
    other_environments = set(
        _ for _ in environments().keys() if _.startswith(f'{env_name}_'))
    for container in dockerClient.containers(
            all=True, filters={'name': f'{env_name}_*'}):
        if not any(
                container.name.startswith(f'{_}_')
                for _ in other_environments):
            dockerClient.rm_container(container.id, wait=False)
    if environment_exists(env_name):
        env_path = get_environment_path(env_name)
        if env_path.exists():
            env_id = (env_path / '.bssenv').read_text().strip()
            # remove all images guard containers
            for container in dockerClient.containers(
                    all=True, filters={'name': f'GUARD_{env_id}_*'}):
                dockerClient.rm_container(container.id, wait=False)
            # remove environment files
            # trick to rm environment files owned accidentally by
            # root or the other user
            exec2(
                ['docker', 'run', '--rm',
                 '-v', f'{env_path}:/rm_me',
                 'alpine:latest',
                 'sh', '-c', 'rm -rf /rm_me/* /rm_me/.*'])
            remove_path(env_path)
        # remove from environments registry
        rm_environment_from_environments_file(env_name)
    # remove docker network
    network_name = f'{env_name}_network'
    if dockerClient.network_exists(network_name):
        dockerClient.rm_network(network_name)
