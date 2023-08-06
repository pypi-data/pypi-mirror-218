# imports from normal python site packages
import sys
import os
import stat
import threading
from pathlib import Path
from contextlib import ExitStack
from typing import Dict, Optional
import local.composefile
import local.services
import local.install
import local.os
import local.yaml
from local.logging import info, debug
from local.paths import \
    ENV_MAIN_LOG_FILE, ENV_COMMAND_REGISTRY_FILE, ENV_BIN_DIR, \
    ENV_COMMAND_REGISTRY_DIR, ENV_AUTOCOMPLETION_DIR, ENV_LOCKS_DIR, ENV_DIR
from local.entities import SERVICE_TYPES, Service, COMMAND_TYPES
from local.cache import Cache, CacheTransformer, FileCacheEntry
from local.docker import dockerClient
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages
import portalocker


lock = threading.RLock()
Cache = Cache()


# {
#     'commands': {
#         'command1': [
#             {'type': 'service'},
#             {'type': 'service_command', 'service_key': 'some_service_key'},
#             {'type': 'service_command', 'service_key': 'some_service_key_2'}
#         ]
#     },
#     'shell_scripts': {
#         'some_script': [
#             {'service_key': 'some_service', 'command_key': 'some_command_key', 'file_path': 'some_file_path'}  # noqa: E501
#         ]
#     }
# }


class CommandRegistryCacheTransformer(CacheTransformer):

    def transform(self) -> Dict:
        if self.value is not None:
            self.value = local.yaml.str_to_dict(self.value or '{}')
            shell_scripts = self.value.get('shell_scripts', {})
            for shell_script in shell_scripts.values():
                for entry in shell_script:
                    entry['file_path'] = ENV_DIR / entry['file_path']
        return self.value


class CommandRegistryFileCacheEntry(
        CommandRegistryCacheTransformer, FileCacheEntry):
    pass


def get_command_registry() -> Dict:
    with lock:
        if not Cache.exists(ENV_COMMAND_REGISTRY_FILE):
            Cache.add(CommandRegistryFileCacheEntry(ENV_COMMAND_REGISTRY_FILE))
        return Cache.get(ENV_COMMAND_REGISTRY_FILE)


def set_command_registry(command_registry: Dict) -> None:
    with lock:
        for shell_script_entries in \
                command_registry.get('shell_scripts', {}).values():
            for entry in shell_script_entries:
                if str(entry['file_path']).startswith(str(ENV_DIR)):
                    entry['file_path'] = \
                        entry['file_path'].relative_to(ENV_DIR)
        ENV_COMMAND_REGISTRY_FILE.write_text(
            local.yaml.dict_to_str(command_registry))


def add_command_to_command_registry(
        service: Service, command_key: Optional[str] = None) -> None:
    type = 'service_command' if command_key else 'service'
    command_registry = get_command_registry() or {}
    command_registry['commands'] = \
        command_registry.get('commands', {})
    commands = command_registry['commands']
    command_entries = commands.get(command_key or service.key, [])
    for entry in command_entries:
        if (
            (entry['type'] == 'service' and type == 'service')
            or (
                entry['type'] == type
                and entry['service_key'] == service.key
            )
        ):
            break
    else:
        command_entries.append({'type': type})
        if type == 'service_command':
            command_entries[-1]['service_key'] = service.key
        commands[command_key or service.key] = command_entries
        set_command_registry(command_registry)


def remove_command_from_command_registry(
        service: Service, command_key: Optional[str] = None) -> None:
    type = 'service_command' if command_key else 'service'
    entries_key = command_key or service.key
    command_registry = get_command_registry() or {}
    command_registry['commands'] = \
        command_registry.get('commands', {})
    commands = command_registry['commands']
    command_entries = commands.get(entries_key, [])
    new_command_entries = []
    do_update = False
    for entry in command_entries:
        if (
            (entry['type'] == 'service' and type == 'service')
            or (
                entry['type'] == type
                and entry['service_key'] == service.key
            )
        ):
            do_update = True
        else:
            new_command_entries.append(entry)
    if do_update:
        if len(new_command_entries) > 0:
            commands[entries_key] = new_command_entries
        else:
            if entries_key in commands.keys():
                del commands[entries_key]
        set_command_registry(command_registry)


def add_shell_script_to_command_registry(
        service: Service, shell_script_name: str, shell_script: str,
        command_key: Optional[str] = None) -> None:
    # create shell script
    uuid = \
        service.commands[command_key]['uuid'] \
        if command_key else service.bssenv['command']['uuid']
    shell_script_symlink_path = ENV_BIN_DIR / shell_script_name
    shell_script_path = ENV_COMMAND_REGISTRY_DIR / uuid
    shell_script_path.write_text(shell_script)
    shell_script_path.chmod(
        shell_script_path.stat().st_mode | stat.S_IEXEC)
    if shell_script_symlink_path.exists() \
            or shell_script_symlink_path.is_symlink():
        shell_script_symlink_path.unlink()
    local.os.create_relative_symbolic_link(
        shell_script_path, shell_script_symlink_path)
    # add registry entry
    command_registry = get_command_registry() or {}
    command_registry['shell_scripts'] = \
        command_registry.get('shell_scripts', {})
    shell_scripts = command_registry['shell_scripts']
    script_entries = [
        _ for _ in shell_scripts.get(shell_script_name, [])
        if not (
            _['service_key'] == service.key
            and (
                (_['command_key'] is None and command_key is None)
                or (_['command_key'] == command_key)
            )
        )
    ]
    script_entries.append(
        {
            'service_key': service.key,
            'command_key': command_key,
            'file_path': shell_script_path
        }
    )
    shell_scripts[shell_script_name] = script_entries
    set_command_registry(command_registry)


def remove_shell_script_from_command_registry(
        service: Service, shell_script_name: str,
        command_key: Optional[str] = None) -> None:
    command_registry = get_command_registry() or {}
    command_registry['shell_scripts'] = \
        command_registry.get('shell_scripts', {})
    shell_scripts = command_registry['shell_scripts']
    script_entries = shell_scripts.get(shell_script_name, [])
    new_script_entries = []
    shell_script_symlink_path = ENV_BIN_DIR / shell_script_name
    for entry in script_entries:
        if (
            entry['service_key'] == service.key
            and (
                (entry['command_key'] is None and command_key is None)
                or (entry['command_key'] == command_key)
            )
        ):
            entry['file_path'].unlink()
        else:
            new_script_entries.append(entry)
    if shell_script_symlink_path.exists() \
            or shell_script_symlink_path.is_symlink():
        shell_script_symlink_path.unlink()
    if len(new_script_entries) < 1:
        if shell_script_name in shell_scripts.keys():
            del shell_scripts[shell_script_name]
    else:
        shell_scripts[shell_script_name] = new_script_entries
        last_entry = new_script_entries[-1]
        local.os.create_relative_symbolic_link(
            last_entry['file_path'], shell_script_symlink_path)
    set_command_registry(command_registry)


def add_autocompletion_to_command_registry(
        service: Service, shell_script_name: str, autocompletion_body: str,
        command_key: Optional[str] = None) -> None:
    uuid = \
        service.commands[command_key]['uuid'] \
        if command_key else service.bssenv['command']['uuid']
    # install
    install_symlink_path = \
        ENV_AUTOCOMPLETION_DIR / f"{shell_script_name}.install"
    install_path = ENV_COMMAND_REGISTRY_DIR / f"{uuid}.install"
    install_path.write_text(
        f'{autocompletion_body}\n\n'
        f'complete -F complete_{shell_script_name} {shell_script_name}'
    )
    if install_symlink_path.exists() or install_symlink_path.is_symlink():
        install_symlink_path.unlink()
    local.os.create_relative_symbolic_link(install_path, install_symlink_path)
    # uninstall
    uninstall_symlink_path = \
        ENV_AUTOCOMPLETION_DIR / f"{shell_script_name}.uninstall"
    uninstall_path = ENV_COMMAND_REGISTRY_DIR / f"{uuid}.uninstall"
    uninstall_path.write_text(
        f'complete -p {shell_script_name} &> /dev/null && complete -r {shell_script_name}'  # noqa: E501
    )
    if uninstall_symlink_path.exists() or uninstall_symlink_path.is_symlink():
        uninstall_symlink_path.unlink()
    local.os.create_relative_symbolic_link(
        uninstall_path, uninstall_symlink_path)


def remove_autocompletion_from_command_registry(
        service: Service, shell_script_name: str,
        command_key: Optional[str] = None) -> None:
    command_registry = get_command_registry() or {}
    command_registry['shell_scripts'] = \
        command_registry.get('shell_scripts', {})
    shell_scripts = command_registry['shell_scripts']
    script_entries = shell_scripts.get(shell_script_name, [])
    uuid = \
        service.commands[command_key]['uuid'] \
        if command_key else service.bssenv['command']['uuid']
    # install
    install_symlink_path = \
        ENV_AUTOCOMPLETION_DIR / f"{shell_script_name}.install"
    install_path = ENV_COMMAND_REGISTRY_DIR / f"{uuid}.install"
    if install_symlink_path.exists() or install_symlink_path.is_symlink():
        install_symlink_path.unlink()
    if install_path.exists():
        install_path.unlink()
    # uninstall
    uninstall_symlink_path = \
        ENV_AUTOCOMPLETION_DIR / f"{shell_script_name}.uninstall"
    uninstall_path = ENV_COMMAND_REGISTRY_DIR / f"{uuid}.uninstall"
    if uninstall_symlink_path.exists() or uninstall_symlink_path.is_symlink():
        uninstall_symlink_path.unlink()
    if uninstall_path.exists():
        uninstall_path.unlink()
    if len(script_entries) > 0:
        prev_entry = script_entries[-1]
        prev_service_key = prev_entry['service_key']
        prev_command_key = prev_entry['command_key']
        prev_service = local.install.get_installed_service(
            prev_service_key)
        prev_uuid =  \
            prev_service.commands[prev_command_key]['uuid'] \
            if prev_command_key else prev_service.bssenv['command']['uuid']
        prev_install_path = \
            ENV_COMMAND_REGISTRY_DIR / f"{prev_uuid}.install"
        prev_uninstall_path = \
            ENV_COMMAND_REGISTRY_DIR / f"{prev_uuid}.uninstall"
        if prev_install_path.exists() and prev_uninstall_path.exists():
            local.os.create_relative_symbolic_link(
                prev_install_path, install_symlink_path)
            local.os.create_relative_symbolic_link(
                prev_uninstall_path, uninstall_symlink_path)


def run(service_key: str, *args: str) -> None:
    # TODO: at this moment we assume that each service has one container.
    # But in the future it can be so that command could have more then
    # one instance: bssenv.command.multiple.instances=true/false
    # service.container_name + '_inst_[3]'
    if not local.install.is_installed_service(service_key):
        raise Exception(f'Service "{service_key}" is not installed"')
    service = local.services.get_service(service_key)
    if service.is_command:
        info(f'Run command: {service_key}')
        composefile_path = \
            local.composefile.get_path_for_service_name_composefile(
                service.name, service.main_type)
        if len(args) < 1 \
                and len(service.command_default_args) > 0:
            args = service.command_default_args
        args = service.entrypoint_command + list(args)
        cmd = [
                'docker-compose', 'run', '--rm', '--name',
                service.container_name, service_key, *args]
        env = {**os.environ, 'COMPOSE_FILE': str(composefile_path)}
        debug(str([f'COMPOSE_FILE={composefile_path}', *cmd]))
        if os.environ.get('BSSENV_STDOUT_MODE', 'false') == 'true':
            local.os.run(cmd, env=env)
        else:
            local.os.fexec(cmd, env=env) >> ENV_MAIN_LOG_FILE
    else:
        raise Exception(f'Service key "{service_key}" is not of type'
                        f'"{SERVICE_TYPES.COMMAND.value}"')


def run_service_command(
        service_key: str, command_key: str, *cmd_args: str) -> None:
    if not local.install.is_installed_service(service_key):
        raise Exception(f'Service "{service_key}" is not installed"')
    service = local.install.get_installed_service(service_key)
    command = (service.commands or {}).get(command_key, None)
    if not command:
        raise Exception(
            f'Command "{command_key}" '
            f'not defined for service "{service_key}"')
    if command['type'] == COMMAND_TYPES.EXEC.value and \
            not (
                service.container_name
                and dockerClient.is_running_container(service.container_name)):
        raise Exception(
            f'Command "{command_key}" is of type exec '
            f'but container for "{service_key}" is not running right now')
    info(f'Run command: {command_key}')
    composefile_path = \
        local.composefile.get_path_for_service_name_composefile(
            service.name, service.main_type)
    # docker-compose args
    cmd = ['docker-compose']
    cmd_str = f'COMPOSE_FILE={composefile_path}'
    if command['type'] == COMMAND_TYPES.EXEC.value:
        cmd += ['exec']
    elif command['type'] == COMMAND_TYPES.RUN.value:
        cmd += [
            'run', '--rm',
            '--label', f'bssenv.service.command.key={command_key}'
        ]
    if command.get('compose_args', None):
        for compose_arg in command['compose_args']:
            if isinstance(compose_arg, str):
                if len(compose_arg) > 1:
                    cmd += [f'--{compose_arg}']
                else:
                    cmd += [f'-{compose_arg}']
            else:
                for key, value in compose_arg.items():
                    if len(key) > 1:
                        cmd += [f'--{key}', value]
                    else:
                        cmd += [f'-{key}', value]
    cmd += [service.key]
    # cmd args
    if len(cmd_args) < 1 and command.get('default_args', None):
        cmd_args = command['default_args']
    # cmd
    cmd += [*command['cmd'], *cmd_args]
    for cmd_arg in cmd:
        if ' ' in cmd_arg:
            cmd_str = f'{cmd_str} "{cmd_arg}"'
        else:
            cmd_str = f'{cmd_str} {cmd_arg}'
    with ExitStack() as stack:
        if not command.get('allow_multiple', False):
            # lock one instance if necessary
            debug(
                f'Only one instance of "{command_key}" is allowed. '
                f'Trying to lock')
            lock_file = \
                ENV_LOCKS_DIR / f'{service_key}.{command_key}.lock'
            lock_file.touch()
            stack.enter_context(portalocker.Lock(lock_file, 'a', timeout=10))
        # run
        debug(cmd_str)
        env = {**os.environ, 'COMPOSE_FILE': str(composefile_path)}
        if os.environ.get('BSSENV_STDOUT_MODE', 'false') == 'true':
            local.os.run(cmd, env=env)
        else:
            local.os.fexec(cmd, env=env) >> ENV_MAIN_LOG_FILE
