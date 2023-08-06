# imports from normal python site packages
import sys
import os
import local.env
import local.paths
import local.install
import local.composefile
import local.daemons
import local.commands
import local.data_providers
from pathlib import Path
from contextlib import contextmanager
from typing import List, Set, Dict
from typing_extensions import Literal
from functools import reduce
from operator import or_
from local.docker import dockerClient
from local.entities import Service, SERVICE_TYPES
from local.os import fexec
from local.logging import debug, info
from .docker.dockerCompose import get_container_config_hash, get_service_config_hash
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages
import dask  # noqa: E402
from dask.delayed import Delayed  # noqa: E402


Service_key = str
Service_name = str
Command_key = str


def service_key_to_name(service_key: str) -> str:
    # INFO: only for already installed services
    return local.install.get_installed_service(service_key).name


def service_key_type_to_name(service_key: str, service_type: str) -> str:
    if service_type == SERVICE_TYPES.DATA_PROVIDER.value:
        return service_key \
            .replace('_restore', '') \
            .replace('_compress', '') \
            .replace('_build', '')
    else:
        return service_key


def service_name_type_to_key(service_name: str, service_type: str) -> str:
    if service_type == SERVICE_TYPES.DATA_PROVIDER_BUILD.value:
        return f'{service_name}_build'
    elif service_type == SERVICE_TYPES.DATA_PROVIDER_COMPRESS.value:
        return f'{service_name}_compress'
    elif service_type == SERVICE_TYPES.DATA_PROVIDER_RESTORE.value:
        return f'{service_name}_restore'
    else:
        return service_name


def get_service(service_key: str) -> Service:
    return local.install.get_installed_service(service_key)


def get_service_main_type(service_name: str) -> str:
    for service in local.install.get_installed_services().values():
        if service.name == service_name:
            return service.main_type


def get_service_name_keys(service_name: Service_name) -> Set[Service_key]:
    return set(_.key for _ in local.install.get_installed_services().values() if _.name == service_name)


def stop(*entity_names: str, wait: bool = True):
    service_keys: Set[Service_key] = set()
    service_commands: Dict[Service_key, Set[Command_key]] = dict()
    for entity_name in entity_names:
        if ':' in entity_name:
            service_key, command_key = (entity_name.split(':') + [None])[0:2]
            service_commands[service_key] = service_commands.get(service_key, set())
            service_commands[service_key].add(command_key)
        else:
            service_keys.add(entity_name)
    for service_key in service_keys | service_commands.keys():
        if not local.install.is_installed_service(service_key):
            raise Exception(f'Service "{service_key}" is not installed"')
    if len(service_keys) < 1 and len(service_commands) < 1:
        debug('Stop all services and all service commands of type "run"')
        services = local.install.get_installed_services().values()
        for service in services:
            if service.commands:
                command_keys: Set[Command_key] = set()
                for command_key, command in service.commands.items():
                    if command['type'] == 'run':
                        command_keys.add(command_key)
                if len(command_keys) > 0:
                    service_commands[service.key] = command_keys
    else:
        services = [get_service(_) for _ in service_keys]
    services = [_ for _ in services if _.container_name is not None]
    service_keys = set(_.key for _ in services)
    debug(f'Stop services: {service_keys}')
    debug(f'Stop service commands: {service_commands}')
    debug(f'wait: {wait}')
    running_containers_to_stop: Set[str] = set()
    for service in services:
        if not dockerClient.is_stopped_container(service.container_name):
            running_containers_to_stop.add(dockerClient.container_id(service.container_name))
    if service_commands:
        service_commands_ids = set(
            f'{_}:{__}'
            for _ in service_commands.keys()
            for __ in service_commands[_]
        )
        for container in dockerClient.containers(
                ignore_removed=True, filters={'label': f'bssenv.environment.id={local.env.id()}'}):
            if (
                container.labels.get('bssenv.container.type', None) == 'service'
                and container.labels.get('bssenv.service.command.key', None) is not None
            ):
                command_id = \
                    f'{container.labels["bssenv.service.key"]}:{container.labels["bssenv.service.command.key"]}'
                if command_id in service_commands_ids:
                    running_containers_to_stop.add(container.id)
    if len(running_containers_to_stop) > 0:
        graph = _build_directed_acyclic_graph(*service_keys, service_commands=service_commands, graph_type='stop')
        graph.compute()
        if wait:
            for container_id in running_containers_to_stop:
                info(f'Wait until stopped container: {container_id}')
                dockerClient.wait_untill_stopped_container(container_id)
    else:
        debug('Nothing to stop')


@dask.delayed
def _wait_untill_stopped_dag_node(
        service_key: Service_key,
        *dependencies: Delayed) -> None:
    service = get_service(service_key)
    if service.container_name is not None:
        info(f'Waiting until service "{service_key}" is stopped')
        debug(f'dependencies length: {len(dependencies)}')
        dockerClient.wait_untill_stopped_container(service.container_name, timeout=300)


@dask.delayed
def _wait_untill_running_dag_node(
        service_key: Service_key,
        *dependencies: Delayed) -> None:
    service = get_service(service_key)
    if service.container_name is not None:
        info(f'Waiting until service "{service_key}" is started')
        debug(f'dependencies length: {len(dependencies)}')
        dockerClient.wait_until_running_container(service.container_name, timeout=300)


@dask.delayed
def _wait_untill_healthy_dag_node(service_key: Service_key, *dependencies: Delayed) -> None:
    service = get_service(service_key)
    if service.container_name is not None:
        info(f'Waiting until service "{service_key}" is healthy')
        debug(f'dependencies length: {len(dependencies)}')
        dockerClient.wait_untill_healthy_container(service.container_name, timeout=300)


@dask.delayed
def _start_dag_node(
        service_key: Service_key,
        *dependencies: Delayed,
        cmd_args: List[str] = None) -> None:
    service = get_service(service_key)
    debug(f'Start service: {service.key}')
    debug(f'service.main_type: {service.main_type}')
    debug(f'cmd_args: {cmd_args}')
    debug(f'dependencies length: {len(dependencies)}')
    if service.main_type == SERVICE_TYPES.DAEMON.value:
        local.daemons.up(service.key)
    elif service.main_type == SERVICE_TYPES.COMMAND.value:
        local.commands.run(service.key, *(cmd_args or []))
    elif service.main_type == SERVICE_TYPES.DATA_PROVIDER.value:
        if SERVICE_TYPES.DATA_PROVIDER_BUILD.value in service.types:
            local.data_providers.build(service.key)
        elif SERVICE_TYPES.DATA_PROVIDER_RESTORE.value in service.types:
            local.data_providers.restore(service.key)
        elif SERVICE_TYPES.DATA_PROVIDER_COMPRESS.value in service.types:
            local.data_providers.compress(service.key)


@dask.delayed
def _start_service_command_dag_node(
        service_key: Service_key,
        command_key: Command_key,
        *dependencies: Delayed,
        cmd_args: List[str] = None) -> None:
    debug(f'service_key: {service_key}')
    debug(f'command_key: {command_key}')
    debug(f'cmd_args: {cmd_args}')
    debug(f'dependencies length: {len(dependencies)}')
    local.commands.run_service_command(service_key, command_key, *(cmd_args or []))


@dask.delayed
def _stop_dag_node(service_key: Service_key, *dependencies: Delayed) -> None:
    service = get_service(service_key)
    if service.container_name:
        debug(f'Stop service: {service.key}')
        debug(f'Stop container: {service.container_name}')
        debug(f'service.main_type: {service.main_type}')
        debug(f'dependencies length: {len(dependencies)}')
        dockerClient.stop_container(service.container_name, timeout=service.stop_grace_period)


@dask.delayed
def _stop_service_command_container_dag_node(container_id: str, *dependencies: Delayed) -> None:
    debug(f'Stop container: {container_id}')
    dockerClient.stop_container(container_id)


def _get_start_services(*service_keys: Service_key) -> Set[Service_key]:
    debug(f'service_keys: {service_keys}')
    if len(service_keys) > 0:
        start_dependencies = reduce(
            or_,
            (
                _.start_dependencies | _.start_healthy_dependencies
                for _ in local.install.get_installed_services().values() if _.key in service_keys
            ),
            set()
        )
        if len(start_dependencies) > 0:
            return set(service_keys) | _get_start_services(*start_dependencies)
        else:
            return set(service_keys)
    else:
        return set()


def _get_stop_services_from_stop_deps(*service_keys: Service_key) -> Set[Service_key]:
    debug(f'service_keys: {service_keys}')
    if len(service_keys) > 0:
        return reduce(
            or_,
            (
                _.stop_dependencies for _ in local.install.get_installed_services().values() if _.key in service_keys
            ),
            set()
        )
    else:
        return set()


def _get_stop_services_from_reversed_start_deps(*service_keys: Service_key) -> Set[Service_key]:
    debug(f'service_keys: {service_keys}')
    if len(service_keys) > 0:
        service_keys = set(service_keys)
        reversed_start_deps = [
            _.key for _ in local.install.get_installed_services().values()
            if ((_.start_dependencies | _.start_healthy_dependencies) & service_keys)]
        if len(reversed_start_deps) > 0:
            return service_keys | _get_stop_services_from_reversed_start_deps(*reversed_start_deps)
        else:
            return set(service_keys)
    else:
        return set()


def _build_directed_acyclic_graph(
        *service_keys: Service_key,
        service_commands: Dict[Service_key, Set[Command_key]] = None,
        keep_running_daemons: bool = True,
        graph_type: Literal['start', 'stop'] = 'start',
        cmd_args: List[str] = None) -> Delayed:
    service_keys: Set[str] = set(service_keys)
    if graph_type == 'start':
        # which services to start?:
        #  1. services provided as argument (service_keys)
        #  and:
        start_service_commands: Dict[Service_key, Set[Command_key]] = dict()
        for service_key in (service_commands or dict()).keys():
            for command_key in (service_commands[service_key] or set()):
                debug(f'{service_key}:{command_key}')
                service = get_service(service_key)
                command = (service.commands or {}).get(command_key, None)
                if command:
                    start_service_commands[service_key] = start_service_commands.get(service_key, set())
                    start_service_commands[service_key].add(command_key)
                    if command['type'] == 'exec':
                        #  2. + parent services for service commands of type
                        #       exec (service_commands)
                        service_keys.add(service_key)
                    else:
                        #  3. + services from start dependencies of parent
                        #       services for service commands of type 'run'
                        #       (service_commands)
                        service_keys |= service.start_dependencies | service.start_healthy_dependencies
                    debug(f'service_keys: {service_keys}')
                else:
                    raise Exception(f'Command "{command_key}" not defined for service "{service_key}"')
        #  and:
        if keep_running_daemons:
            #  4. + already running services
            service_keys |= set([
                _.key for _ in local.install.get_installed_services().values()
                if _.is_daemon and dockerClient.is_running_container(_.container_name)
            ])
            debug(f'service_keys with running daemons: {service_keys}')
        #  and:
        #  5. + all start dependencies from services that are planned to
        #       be started
        start_services = _get_start_services(*service_keys)
        # which services to stop?:
        #  1. all stop dependencies from services that are planned
        #     to be started
        stop_services = _get_stop_services_from_stop_deps(*start_services)
        #  2.  + services that have any of the stop services in their
        #        required start dependencies (that services can't be running
        #        without services we plan to stop)
        stop_services |= _get_stop_services_from_reversed_start_deps(*stop_services)
        # do not stop any of the service commands provided:
        stop_service_commands: Set[str] = set()
    else:
        # which services to stop?:
        #  1. services provided as argument (service_keys)
        #  and:
        #  2.  + services that have any of the service keys planned
        #        to be stopped in their required start dependencies (that
        #        services can't be running without services we plan to stop)
        stop_services = _get_stop_services_from_reversed_start_deps(*service_keys)
        #  3.  + all running containers for service commands if provided
        stop_service_commands: Set[str] = set()
        service_commands_running_containers: Dict[str, str] = dict()
        if service_commands:
            service_commands_running_containers = {
                f'{_.labels["bssenv.service.key"]}:{_.labels["bssenv.service.command.key"]}': _.id  # noqa: E501
                for _ in dockerClient.containers(
                    ignore_removed=True,
                    filters={'label': f'bssenv.environment.id={local.env.id()}'})  # noqa: E501
                if (
                    _.labels.get('bssenv.container.type', None) == 'service'
                    and _.labels.get('bssenv.service.command.key', None) is not None
                )
            }
            for service_key in service_commands.keys():
                for command_key in (service_commands[service_key] or set()):
                    command_id = f'{service_key}:{command_key}'
                    if command_id in service_commands_running_containers.keys():
                        stop_service_commands.add(command_id)
        # nothing to start:
        start_services: Set[Service_key] = set()
        start_service_commands: Dict[Service_key, Set[Command_key]] = dict()
    start_services = set(_ for _ in start_services if local.install.is_installed_service(_))
    stop_services = set(_ for _ in stop_services if local.install.is_installed_service(_))
    debug(f'start_services: {start_services}')
    debug(f'stop_services: {stop_services}')
    debug(f'start_service_commands: {start_service_commands}')
    debug(f'stop_service_commands: {stop_service_commands}')
    # services that needs to be stopped during graph execution
    # but also needs to be started at the end
    stop_and_start_services = stop_services & start_services
    debug(f'stop_and_start_services: {stop_and_start_services}')
    start_services_entities = [get_service(_) for _ in start_services]
    all_nodes = []
    wait_stopped_nodes = dict()
    wait_stopped_after_start_nodes = dict()
    wait_running_nodes = dict()
    wait_healthy_nodes = dict()
    while \
            len(stop_services) > 0 or \
            len(stop_service_commands) > 0 or \
            len(start_services) > 0 or \
            len(start_service_commands) > 0:
        is_infinite_loop = True
        # stop services
        for service_key in stop_services.copy():
            service = get_service(service_key)
            dependent_nodes = []
            wait_stopped_from_reversed_start_deps = set(
                _ for _, __ in local.install.get_installed_services().items()
                if service_key in __.start_dependencies | __.start_healthy_dependencies)
            debug(f'wait_stopped_from_reversed_start_deps: {wait_stopped_from_reversed_start_deps}')
            if all(_ in wait_stopped_nodes.keys() for _ in wait_stopped_from_reversed_start_deps):
                for _ in wait_stopped_from_reversed_start_deps:
                    dependent_nodes += [wait_stopped_nodes[_]]
                stop_node = _stop_dag_node(service.key, *dependent_nodes)
                all_nodes += [stop_node]
                wait_stopped_nodes[service.key] = _wait_untill_stopped_dag_node(service.key, stop_node)
                stop_services.remove(service.key)
                is_infinite_loop = False
        # stop service commands
        for command_id in stop_service_commands.copy():
            all_nodes.append(
                _stop_service_command_container_dag_node(service_commands_running_containers[command_id]))
            stop_service_commands.remove(command_id)
            is_infinite_loop = False
        # start services
        if not stop_services:
            for service_key in start_services.copy():
                service = get_service(service_key)
                dependent_nodes = []
                wait_running_deps = \
                    set(_ for _ in service.start_dependencies if local.install.is_installed_service(_))
                wait_healthy_deps = \
                    set(_ for _ in service.start_healthy_dependencies if local.install.is_installed_service(_))
                wait_stopped_deps = \
                    set(_ for _ in service.stop_dependencies if local.install.is_installed_service(_))
                wait_stopped_after_start_deps = set()
                if service.key in stop_and_start_services:
                    # this service must be started but it was also
                    # requested by the other service to be stopped at
                    # least for a while
                    for _ in start_services_entities:
                        if _.key != service.key and \
                                service.key in _.stop_dependencies:
                            if _.is_daemon:
                                exit(
                                    f'Service "{service.key}" needs to be started but it was scheduled to '
                                    f'stop by dependent daemon "{_.key}" that is also going to be started')
                            else:
                                # INFO: all entries in all_services are
                                # installed so we do not have to check it
                                # here
                                wait_stopped_after_start_deps |= set([_.key])
                debug(f'wait_stopped_deps: {wait_stopped_deps}')
                debug(f'wait_stopped_after_start_deps: {wait_stopped_after_start_deps}')
                debug(f'wait_running_deps: {wait_running_deps}')
                debug(f'wait_healthy_deps: {wait_healthy_deps}')
                if not (
                    any(_ not in wait_stopped_nodes.keys() for _ in wait_stopped_deps) or
                    any(_ not in wait_stopped_after_start_nodes.keys() for _ in wait_stopped_after_start_deps) or
                    any(_ not in wait_running_nodes.keys() for _ in wait_running_deps) or
                    any(_ not in wait_healthy_nodes.keys() for _ in wait_healthy_deps)
                ):
                    for _ in wait_stopped_deps:
                        dependent_nodes += [wait_stopped_nodes[_]]
                    for _ in wait_stopped_after_start_deps:
                        dependent_nodes += [wait_stopped_after_start_nodes[_]]
                    for _ in wait_running_deps:
                        dependent_nodes += [wait_running_nodes[_]]
                    for _ in wait_healthy_deps:
                        dependent_nodes += [wait_healthy_nodes[_]]
                    if service.key in wait_stopped_nodes:
                        dependent_nodes += [wait_stopped_nodes[service.key]]
                    debug(f'Start_dag: {service.key}: {dependent_nodes}')
                    start_node = _start_dag_node(service.key, *dependent_nodes, cmd_args=cmd_args)
                    all_nodes += [start_node]
                    wait_running_node = _wait_untill_running_dag_node(service.key, start_node)
                    wait_running_nodes[service.key] = wait_running_node
                    wait_healthy_node = _wait_untill_healthy_dag_node(service.key, wait_running_node)
                    wait_healthy_nodes[service.key] = wait_healthy_node
                    wait_stopped_after_start_node = _wait_untill_stopped_dag_node(service.key, start_node)
                    wait_stopped_after_start_nodes[service.key] = wait_stopped_after_start_node
                    start_services.remove(service.key)
                    is_infinite_loop = False
        # start service commands
        if not start_services:
            # for service_key, command_key in \
            #         start_service_commands.copy().items():
            for service_key in start_service_commands.copy().keys():
                for command_key in start_service_commands[service_key].copy():
                    service = get_service(service_key)
                    command = service.commands[command_key]
                    if command['type'] == 'exec':
                        # wait until parent service is started and healthy
                        if service.key in wait_healthy_nodes.keys():
                            # and then run command
                            all_nodes.append(
                                _start_service_command_dag_node(
                                    service.key, command_key, wait_healthy_nodes[service.key], cmd_args=cmd_args))
                            start_service_commands[service_key].remove(command_key)
                            if len(start_service_commands[service_key]) < 1:
                                del start_service_commands[service_key]
                            is_infinite_loop = False
                    else:
                        # wait until parent service start dependencies are
                        # started and healthy
                        wait_running_deps = \
                            set(_ for _ in service.start_dependencies if local.install.is_installed_service(_))
                        wait_healthy_deps = \
                            set(_ for _ in service.start_healthy_dependencies if local.install.is_installed_service(_))
                        if \
                                all(_ in wait_running_nodes.keys() for _ in wait_running_deps) \
                                and all(_ in wait_healthy_nodes.keys() for _ in wait_healthy_deps):
                            # and then run command
                            dependent_nodes = []
                            for _ in wait_running_deps:
                                dependent_nodes.append(wait_running_nodes[_])
                            for _ in wait_healthy_deps:
                                dependent_nodes.append(wait_healthy_nodes[_])
                            all_nodes.append(
                                _start_service_command_dag_node(
                                    service.key, command_key, *dependent_nodes, cmd_args=cmd_args))
                            start_service_commands[service_key].remove(command_key)
                            if len(start_service_commands[service_key]) < 1:
                                del start_service_commands[service_key]
                            is_infinite_loop = False
        if is_infinite_loop:
            raise Exception('Infinite loop detected while building directed acyclic graph')
    # just accumulate to one delayed graph
    graph = dask.delayed(lambda *_: None)(*all_nodes)
    # graph.visualize(filename='graph.svg')
    return graph


def start(
        *entity_names: str,
        wait: bool = True,
        keep_running_daemons: bool = False,
        cmd_args: List[str] = None) -> None:
    service_keys: Set[Service_key] = set()
    service_commands: Dict[Service_key, Set[Command_key]] = dict()
    for entity_name in entity_names:
        if ':' in entity_name:
            service_key, command_key = (entity_name.split(':') + [None])[0:2]
            service_commands[service_key] = service_commands.get(service_key, set())
            service_commands[service_key].add(command_key)
        else:
            service_keys.add(entity_name)
    for service_key in service_keys | service_commands.keys():
        if not local.install.is_installed_service(service_key):
            raise Exception(f'Service "{service_key}" is not installed"')
    if len(service_keys) < 1 and len(service_commands) < 1:
        debug('Start all daemon services')
        service_keys = \
            set(_.key for _ in local.install.get_installed_services().values() if _.is_daemon)
    debug(f'Start services: {service_keys}')
    debug(f'Start service commands: {service_commands}')
    debug(f'wait: {wait}')
    debug(f'cmd_args: {cmd_args}')
    graph = _build_directed_acyclic_graph(
        *service_keys, service_commands=service_commands, graph_type='start',
        keep_running_daemons=keep_running_daemons, cmd_args=cmd_args)
    graph.compute()
    if wait:
        for service in (get_service(_) for _ in service_keys if local.install.is_installed_service(_)):
            # we can wait here only for daemon services because it is risky
            # to also wait for commands or data providers. Why? Because at
            # this point these kind of services could be already stopped just
            # after that we have run them before
            if service.is_daemon:
                info(f'Wait until running container: {service.container_name}')
                dockerClient.wait_until_running_container(service.container_name, timeout=300)


@contextmanager
def keep_running_daemons(log=None) -> None:
    running_daemons = [
        _ for _ in local.install.get_installed_services().values()
        if _.is_daemon and dockerClient.is_running_container(_.container_name)
    ]
    try:
        yield
    finally:
        if len(running_daemons) > 0:
            running_daemons = \
                sorted([_.key for _ in running_daemons if local.install.is_installed_service(_.key)])
            if log:
                log(f'Start daemons: {running_daemons}')
            start(*running_daemons, wait=False)


def recreate_service_container(service: Service):
    composefile_path = local.composefile.get_path_for_service_name_composefile(service.name, service.main_type)
    fexec(
        ['docker-compose', 'up', '--no-start', '--force-recreate', '--no-deps', service.key],
        env={**os.environ, 'COMPOSE_FILE': str(composefile_path)}) \
        >> local.paths.ENV_MAIN_LOG_FILE


def is_service_container_outdated(service_key: str) -> bool:
    service = get_service(service_key)
    if dockerClient.container_exists(service.container_name):
        composefile_path = local.composefile.get_path_for_service_name_composefile(service.name, service.main_type)
        container_config_hash = get_container_config_hash(service.container_name)
        config_hash = get_service_config_hash(service.key, composefile_path)
        return container_config_hash != config_hash
    return False


def get_daemons_with_outdated_containers() -> List[Service]:
    outdated_daemons = []
    daemons_with_containers = [
        _ for _ in local.install.get_installed_services().values()
        if _.is_daemon and dockerClient.container_exists(_.container_name)]
    if len(daemons_with_containers) > 0:
        service_keys_to_check = [service.key for service in daemons_with_containers]
        containers_to_check = [service.container_name for service in daemons_with_containers]
        container_config_hashes = get_container_config_hash(*containers_to_check)
        config_hashes = get_service_config_hash(
            *service_keys_to_check, composefile_path=local.paths.ENV_COMPOSEFILES_DIR / 'daemons.yml')
        for i in range(0, len(daemons_with_containers)):
            daemon = daemons_with_containers[i]
            if container_config_hashes[i] != config_hashes[i]:
                outdated_daemons.append(daemon)
    return outdated_daemons
