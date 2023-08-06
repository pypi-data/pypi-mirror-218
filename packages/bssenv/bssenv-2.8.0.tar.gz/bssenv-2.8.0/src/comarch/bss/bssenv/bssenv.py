#!/usr/bin/env python3


# imports from normal python site packages
import sys
import uuid
from os import execlp
from pathlib import Path
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
BSSENV_PKG_PATH = Path(BSSENV_PKG.__file__).resolve().parent
BSSENV_PKG_PYT_SITE_PKGS = BSSENV_PKG_PATH / 'data/python_site_packages'
BSSENV_PKG_LIBS_DIR = BSSENV_PKG_PATH / 'data/scripts/lib/python'
sys.path = [str(BSSENV_PKG_PYT_SITE_PKGS), str(BSSENV_PKG_LIBS_DIR)] + sys.path

# import from custom site packages
import local.bssenv
import local.snapshots
from local.docker import dockerClient, dockerRegistry
from local.commandline import arg, raise_arg_is_required
from local.paths import BSSENV_GLOBAL_TMP_DIR
from local.itertools import each
import humanize
from rich.console import Console
from rich.table import Table
from rich import box, print as rprint


# TODO: dodac: bssenv snapshot push


def print_help():
    print(
        'Show commands info or activate, list and create bssenv environment\n'
        '\n'
        'bssenv info - show short listing of available commands\n'
        'bssenv info2 - show long listing of available commands\n'
        'bssenv list - list all environments\n'
        'bssenv snapshot list - list all local environment snapshots\n'
        'bssenv snapshot list remote - list all remote environment snapshots\n'
        'bssenv snapshot details snapshot_name - '
        'show details about local snapshot "snapshot_name"\n'
        'bssenv snapshot details remote snapshot_name - '
        'show details about remote snapshot "snapshot_name"\n'
        'bssenv activate environment_name - activate environment_name\n'
        'bssenv create env_name - create environment "env_name"\n'
        'bssenv create env_name from snapshot snapshot_name - '
        'create environment "env_name" from snapshot "snapshot_name"\n'
        'bssenv create env_name from remote snapshot snapshot_name - '
        'create environment "env_name" from remote snapshot "snapshot_name"\n'
        'bssenv rm env_name - remove environment "env_name"')


def print_info():
    info = (BSSENV_PKG_PATH / 'data/resources/info') \
            .read_text() \
            .replace('{local.bssenv.version}', local.bssenv.VERSION)
    print(info)


def print_info2():
    info2 = (BSSENV_PKG_PATH / 'data/resources/info2') \
            .read_text() \
            .replace('{local.bssenv.version}', local.bssenv.VERSION)
    print(info2)


def print_post_create_environment_info(env_name: str) -> None:
    post_create_info = (
        BSSENV_PKG_PATH / 'data/resources/post_create_environment_info') \
            .read_text() \
            .replace('{env_name}', env_name)
    print(post_create_info)


def print_post_create_environment_from_snap_info(env_name: str) -> None:
    post_create_info = (
        BSSENV_PKG_PATH /
        'data/resources/post_create_environment_from_snap_info') \
            .read_text() \
            .replace('{env_name}', env_name)
    print(post_create_info)


def run() -> None:
    if any(_ in ['?', '--help', '-h'] for _ in sys.argv[1:]):
        print_help()
        exit()
    elif arg(1) == 'activate':
        env_name = arg(2)
        if not env_name:
            print_help()
            print('\n')
            raise_arg_is_required('environment_name')
        activate = local.bssenv.get_environment_path(env_name) / \
            '.venv/bin/activate'
        local.os.create_dir(BSSENV_GLOBAL_TMP_DIR)
        bashrc_tmp = BSSENV_GLOBAL_TMP_DIR / f'bashrc.{uuid.uuid4()}'
        bashrc_tmp.write_text(
            f'source ~/.bashrc\n'
            f'source "{activate}"\n'
            f'rm "{bashrc_tmp}"')
        execlp('bash', sys.argv[0], '--rcfile', str(bashrc_tmp))
    elif arg(1) == 'info':
        print_info()
    elif arg(1) == 'info2':
        print_info2()
    elif arg(1) == 'list':
        environments = local.bssenv.environments()
        for env_name in sorted(environments.keys()):
            print(f'{env_name} -> source {environments[env_name]}/.venv/bin/activate')
    elif arg(1) == 'create':
        env_name = arg(2)
        if not env_name:
            print_help()
            print()
            exit('Please provide environment name')
        elif env_name == 'data':
            exit(
                '"data" is a restricted word and can not be used as '
                'an environment name')
        if arg(3) is None:
            local.bssenv.create_environment(env_name, Path.cwd())
            print_post_create_environment_info(env_name)
        elif arg(3) == 'from' and arg(4) == 'snapshot':
            snapshot_name = arg(5)
            local.bssenv.create_environment_from_snapshot(
                env_name, snapshot_name, Path.cwd())
            print_post_create_environment_from_snap_info(env_name)
        elif arg(3) == 'from' and arg(4) == 'remote' and arg(5) == 'snapshot':
            snapshot_name = arg(6)
            local.bssenv.create_environment_from_snapshot(
                env_name, snapshot_name, Path.cwd(), True)
            print_post_create_environment_from_snap_info(env_name)
        else:
            print_help()
            print()
            exit('Wrong parameters provided')
    elif arg(1) == 'rm':
        env_name = arg(2)
        if not env_name:
            print_help()
            print()
            exit('Please provide environment name')
        local.bssenv.rm_environment(env_name)
    elif arg(1) == 'snapshot' and arg(2) == 'list':
        console = Console()
        local_or_remote = None
        if arg(3) == 'remote':
            local_or_remote = 'Remote'
            snapshots = local.snapshots.get_remote_snapshots()
        else:
            local_or_remote = 'Local'
            snapshots = local.snapshots.get_local_snapshots()
        headers = ['Name', 'Type', 'Date', 'Service name', 'Environment name']
        rows = []
        for metadata in sorted(snapshots, key=lambda _: _.snapshot_name):
            rows.append([metadata.snapshot_name, metadata.type, metadata.date,
                        metadata.service_name, metadata.environment_name])
        rprint(f'[italic]{local_or_remote} snapshots:')
        table = Table(box=box.SIMPLE)
        each(headers, table.add_column)
        each(rows, table.add_row, expand='args')
        console.print(table)
    elif arg(1) == 'snapshot' and arg(2) == 'details':
        console = Console()
        local_or_remote = None
        if arg(3) == 'remote':
            local_or_remote = 'Remote'
            snapshot_name = arg(4)
            snapshot_metadata = \
                local.snapshots.get_snapshot_metadata(snapshot_name, True)
        else:
            local_or_remote = 'Local'
            snapshot_name = arg(3)
            snapshot_metadata = \
                local.snapshots.get_snapshot_metadata(snapshot_name)
        # describe snapshot
        rprint('[italic]Snapshot:')
        table = Table(show_header=False, box=box.SIMPLE)
        headers = ['key', 'value']
        rows = [
            ['id', snapshot_metadata.id],
            ['name', snapshot_metadata.snapshot_name],
            ['type', snapshot_metadata.type],
            ['date', snapshot_metadata.date],
            (['service name', snapshot_metadata.service_name]
             if snapshot_metadata.service_name
             else ['environment name', snapshot_metadata.environment_name]),
            ['metadata image', snapshot_metadata.meta_image]]
        each(headers, table.add_column)
        each(rows, table.add_row, expand='args')
        console.print(table)
        # describe images
        headers = ['Name', 'Size']
        rows = []
        for image in sorted(snapshot_metadata.images):
            size = dockerClient.get_image_virtual_size(image) \
                if local_or_remote == 'Local' \
                else dockerRegistry.get_image_virtual_size(image)
            rows.append([
                image,
                humanize.naturalsize(size) if size else '???'
            ])
        rprint('[italic]Snapshot images:')
        table = Table(box=box.SIMPLE)
        each(headers, table.add_column)
        each(rows, table.add_row, expand='args')
        console.print(table)
    else:
        print_help()
        print()
        exit('Wrong parameters provided')


if __name__ == '__main__':
    run()
