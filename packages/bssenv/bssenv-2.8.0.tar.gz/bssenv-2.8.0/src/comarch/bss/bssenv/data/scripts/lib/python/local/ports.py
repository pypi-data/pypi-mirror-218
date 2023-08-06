# imports from normal python site packages
import sys
import threading
from pathlib import Path
from typing import Set, Dict, Union
from local.cache import FileCacheEntry, Cache
import local.paths
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages
import port_for  # noqa: E402


lock = threading.RLock()
Cache = Cache()
MIN_PORT = 1024
MAX_PORT = 65535
ENV_CHANGED_PORT_MAPPINGS_FILE = local.paths.ENV_CHANGED_PORT_MAPPINGS_FILE
Service_key = str
Port_name = str
Port_host_value = int


def get_changed_port_mappings() -> Dict[
        Service_key, Dict[Port_name, Port_host_value]]:
    with lock:
        if not Cache.exists(ENV_CHANGED_PORT_MAPPINGS_FILE):
            Cache.add(FileCacheEntry(ENV_CHANGED_PORT_MAPPINGS_FILE))
        port_mappings = dict()
        for line in Cache.get(ENV_CHANGED_PORT_MAPPINGS_FILE).splitlines():
            service_key, port_name, port_host_value = line.split(':')
            service_mappings = port_mappings.get(service_key, dict())
            service_mappings[port_name] = int(port_host_value) \
                if port_host_value else None
            port_mappings[service_key] = service_mappings
        return port_mappings


def set_changed_port_mappings(port_mappings: Dict[
        Service_key, Dict[Port_name, Union[Port_host_value, None]]]) -> None:
    with lock:
        ENV_CHANGED_PORT_MAPPINGS_FILE.write_text("\n".join(
            f'{service_key}:{port_name}:{port_host_value or ""}'
            for service_key, service_mappings in port_mappings.items()
            for port_name, port_host_value in service_mappings.items()))


def add_changed_port_mappings(port_mappings: Dict[
        Service_key, Dict[Port_name, Union[Port_host_value, None]]]) -> None:
    all_port_mappings = get_changed_port_mappings()
    for service_key, service_mappings in port_mappings.items():
        service_mappings = {
            **all_port_mappings.get(service_key, dict()),
            **service_mappings}
        all_port_mappings[service_key] = service_mappings
    set_changed_port_mappings(all_port_mappings)


def add_changed_port_mapping(
        service_key: str, port_name: str, port_host_value:
        Union[int, None]) -> None:
    port_mappings = get_changed_port_mappings()
    service_mappings = port_mappings.get(service_key, dict())
    service_mappings[port_name] = port_host_value
    port_mappings[service_key] = service_mappings
    set_changed_port_mappings(port_mappings)


def remove_changed_port_mappings(
        port_mappings: Union[
            Dict[Service_key, Set[Port_name]],
            None] = None) -> None:
    if port_mappings is None:
        with lock:
            ENV_CHANGED_PORT_MAPPINGS_FILE.write_text('')
    else:
        all_port_mappings = get_changed_port_mappings()
        for service_key, port_names in port_mappings.items():
            if service_key in all_port_mappings.keys():
                service_mappings = all_port_mappings[service_key]
                for port_name in port_names:
                    if port_name in service_mappings.keys():
                        del service_mappings[port_name]
                if len(service_mappings.keys()) < 1:
                    del all_port_mappings[service_key]
        set_changed_port_mappings(all_port_mappings)


def remove_changed_port_mapping(
        service_key: str, port_name: Union[str, None] = None) -> None:
    # if port_name is None then remove all mappings for given service
    port_mappings = get_changed_port_mappings()
    if service_key in port_mappings.keys():
        service_mappings = port_mappings[service_key]
        for mapping_port_name in list(service_mappings.keys()):
            if port_name is None or mapping_port_name == port_name:
                del service_mappings[mapping_port_name]
        if len(service_mappings.keys()) < 1:
            del port_mappings[service_key]
    set_changed_port_mappings(port_mappings)


def get_free_port(start: int = MIN_PORT, exclude: Set[int] = set()) -> int:
    for port in range(start, MAX_PORT):
        if port not in exclude and not port_for.port_is_used(port):
            return port
