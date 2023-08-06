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


lock = threading.RLock()
Cache = Cache()
ENV_SWITCHES_FILE = local.paths.ENV_SWITCHES_FILE
Service_key = str
Switch_name = str
Switch_value = bool


def get_switch_configurations() -> Dict[
        Service_key, Dict[Switch_name, Switch_value]]:
    with lock:
        if not Cache.exists(ENV_SWITCHES_FILE):
            Cache.add(FileCacheEntry(ENV_SWITCHES_FILE))
        switch_configs = dict()
        for line in Cache.get(ENV_SWITCHES_FILE).splitlines():
            service_key, switch_name, switch_value = line.split(':')
            service_switches = switch_configs.get(service_key, dict())
            service_switches[switch_name] = (switch_value.lower() == 'true') \
                if switch_value else False
            switch_configs[service_key] = service_switches
        return switch_configs


def set_switch_configurations(switch_configs: Dict[
        Service_key, Dict[Switch_name, Union[Switch_value, None]]]) -> None:
    with lock:
        ENV_SWITCHES_FILE.write_text("\n".join(
            f'{service_key}:{switch_name}:{switch_value or "false"}'
            for service_key, service_switches in switch_configs.items()
            for switch_name, switch_value in service_switches.items()))


def add_switch_configurations(switch_configs: Dict[
        Service_key, Dict[Switch_name, Union[Switch_value, None]]]) -> None:
    all_switch_configs = get_switch_configurations()
    for service_key, service_switch_configs in switch_configs.items():
        service_switch_configs = {
            **all_switch_configs.get(service_key, dict()),
            **service_switch_configs}
        all_switch_configs[service_key] = service_switch_configs
    set_switch_configurations(all_switch_configs)


def add_switch_configuration(
        service_key: str, switch_name: str, switch_value: bool) -> None:
    switch_configs = get_switch_configurations()
    service_switch_configs = switch_configs.get(service_key, dict())
    service_switch_configs[switch_name] = switch_value
    switch_configs[service_key] = service_switch_configs
    set_switch_configurations(switch_configs)


def remove_switch_configurations(
        switch_configs: Union[
            Dict[Service_key, Set[Switch_name]],
            None] = None) -> None:
    if switch_configs is None:
        with lock:
            ENV_SWITCHES_FILE.write_text('')
    else:
        all_switch_configs = get_switch_configurations()
        for service_key, switch_names in switch_configs.items():
            if service_key in all_switch_configs.keys():
                service_switch_configs = all_switch_configs[service_key]
                for switch_name in switch_names:
                    if switch_name in service_switch_configs.keys():
                        del service_switch_configs[switch_name]
                if len(service_switch_configs.keys()) < 1:
                    del all_switch_configs[service_key]
        set_switch_configurations(all_switch_configs)


def remove_switch_configuration(
        service_key: str, switch_name: Union[str, None] = None) -> None:
    # if switch_name is None then remove all switches configurations
    switch_configs = get_switch_configurations()
    if service_key in switch_configs.keys():
        service_switch_configs = switch_configs[service_key]
        for service_switch_name in list(service_switch_configs.keys()):
            if switch_name is None or service_switch_name == switch_name:
                del service_switch_configs[service_switch_name]
        if len(service_switch_configs.keys()) < 1:
            del switch_configs[service_key]
    set_switch_configurations(switch_configs)
