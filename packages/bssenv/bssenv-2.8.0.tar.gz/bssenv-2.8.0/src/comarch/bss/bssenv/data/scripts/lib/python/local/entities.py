# imports from normal python site packages
import sys
import shlex
from pathlib import Path
from os.path import expandvars
from typing import Dict, List, Set, Union, Iterable, Literal, Optional
import local.os
from local.types import Enumerator
from local.lazy import lazy_property
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


Remote = str
Local = str
Environment = str
Service = str
Service_name = str


class COMPOSEFILE_TYPES(Enumerator):
    DAEMON: str = 'daemon'
    COMMAND: str = 'command'
    DATA_PROVIDER: str = 'data_provider'


class ENTITY_TYPES(Enumerator):
    SERVICE: str = 'service'
    CONFIGMAP: str = 'configmap'


class SERVICE_TYPES(Enumerator):
    DAEMON: str = 'daemon'
    COMMAND: str = 'command'
    DATA_PROVIDER: str = 'data_provider'
    DATA_PROVIDER_RESTORE: str = 'data_provider.restore'
    DATA_PROVIDER_COMPRESS: str = 'data_provider.compress'
    DATA_PROVIDER_BUILD: str = 'data_provider.build'


class CONFIG_MAP_TYPES(Enumerator):
    FILE: str = 'file'
    ENV: str = 'env'


class SERVICE_CATEGORIES(Enumerator):
    INTERNAL: str = 'internal'
    EXTERNAL: str = 'external'


class SNAPSHOT_TYPES(Enumerator):
    ENVIRONMENT: str = 'environment'
    SERVICE: str = 'service'
    CONFIG_MAP: str = 'config_map'


class INIT_TYPES(Enumerator):
    ONETIME: str = 'onetime'
    ALWAYS: str = 'always'


class COMMAND_TYPES(Enumerator):
    RUN: str = 'run'
    EXEC: str = 'exec'


def _get_labels_as_dict(labels: Iterable[str]) -> Dict[str, str]:
    return {k: v for k, _, v in (label.partition('=') for label in labels)}


# DEPRECATED: bssenv.service_type is deprecated
def _get_service_types_from_image_labels(labels: Dict[str, str]) -> Set[str]:
    service_types = labels.get('bssenv.service_type', None)
    return set(
        _ for _ in service_types.split(';')
        if _ in SERVICE_TYPES) \
        if service_types is not None else set()


# DEPRECATED bssenv.service_type is deprecated
def _get_service_categories_from_image_labels(
        labels: Dict[str, str]) -> Set[str]:
    service_types = labels.get('bssenv.service_type', None)
    return set(
        _ for _ in service_types.split(';')
        if _ not in SERVICE_TYPES) \
        if service_types is not None else set()


def _get_final_service_name(
        service_key: str,
        is_data_provider_builder: bool,
        is_data_provider_compressor: bool,
        is_data_provider_restorer: bool) -> str:
    service_name = service_key
    if is_data_provider_builder and service_name.endswith('_build'):
        service_name = service_name[0:-6]
    elif is_data_provider_compressor and service_name.endswith('_compress'):
        service_name = service_name[0:-9]
    elif is_data_provider_restorer and service_name.endswith('_restore'):
        service_name = service_name[0:-8]
    return service_name


class InstalledEntitiesEntry:
    key: str
    image_sha: str
    image_name: str


class InstalledServicesEntry(InstalledEntitiesEntry):
    name: str
    type: Literal['daemon', 'command', 'data_provider']
    image_guard_container: str


class InstalledConfigMapsEntry(InstalledEntitiesEntry):
    type: Literal['file', 'env']


class DescriptorMember:
    type: Literal['service', 'configmap']
    name: str
    is_default: bool
    labels: Dict[str, str]
    image: str
    descriptor_image: str


class SimpleConfigMap(DescriptorMember):
    type = ENTITY_TYPES.CONFIGMAP.value
    cm_tyoe: Literal['file', 'env']
    path: str


class SimpleService(DescriptorMember):
    type = ENTITY_TYPES.SERVICE.value
    types: Set[Literal[
            'daemon', 'command', 'data_provider',
            'data_provider.restore', 'data_provider.compress',
            'data_provider.build']]


class Service:

    __key: str
    __composefile_entry: Dict

    @staticmethod
    def from_dict(service_key: str, service: Dict):
        instance = Service()
        instance.__key = service_key
        instance.__composefile_entry = service
        if 'x-bssenv'not in instance.__composefile_entry.keys():
            instance.__composefile_entry['x-bssenv'] = dict()
        if 'service' not in instance.__composefile_entry['x-bssenv'].keys():
            instance.__composefile_entry['x-bssenv']['service'] = dict()
        return instance

    @property
    def key(self) -> str:
        return self.__key

    @lazy_property
    def name(self) -> str:
        return _get_final_service_name(
            self.key,
            self.is_data_provider_builder,
            self.is_data_provider_compressor,
            self.is_data_provider_restorer)

    @property
    def composefile_entry(self) -> Dict:
        return self.__composefile_entry

    @property
    def bssenv(self) -> Dict:
        return self.composefile_entry['x-bssenv']

    @property
    def service(self) -> Dict:
        return self.bssenv['service']

    @lazy_property
    def types(self) -> Set[str]:
        service_types = _get_service_types_from_image_labels(self.labels)
        if self.service.get('type', None):
            service_types.add(self.service['type'])
        if self.service.get('data_provider', {}).get('type', None):
            service_types.add(self.service['data_provider']['type'])
        return {_ for _ in service_types if _ in SERVICE_TYPES}

    @lazy_property
    def type(self) -> Optional[str]:
        for type in self.types:
            if type in {
                SERVICE_TYPES.DAEMON.value,
                SERVICE_TYPES.COMMAND.value,
                SERVICE_TYPES.DATA_PROVIDER.value
            }:
                self.service['type'] = type
            elif type in {
                SERVICE_TYPES.DATA_PROVIDER_BUILD.value,
                SERVICE_TYPES.DATA_PROVIDER_COMPRESS.value,
                SERVICE_TYPES.DATA_PROVIDER_RESTORE.value
            }:
                self.service['type'] = SERVICE_TYPES.DATA_PROVIDER.value
        return self.service.get('type', None)

    # DEPRECATED: use "type" property instead
    @property
    def main_type(self) -> Optional[str]:
        return self.type

    @lazy_property
    def data_provider_type(self) -> Optional[str]:
        for type in self.types:
            if type in {
                SERVICE_TYPES.DATA_PROVIDER_BUILD.value,
                SERVICE_TYPES.DATA_PROVIDER_COMPRESS.value,
                SERVICE_TYPES.DATA_PROVIDER_RESTORE.value
            }:
                self.service['data_provider'] = \
                    self.service.get('data_provider', {})
                self.service['data_provider']['type'] = type
        return self.service.get('data_provider', {}).get('type', None)

    @lazy_property
    def labels(self) -> Dict[str, str]:
        return _get_labels_as_dict(self.composefile_entry.get('labels', []))

    def add_label(self, key: str, value: str) -> None:
        self.labels[key] = value
        self.composefile_entry['labels'] = [
            f"{_}={__}" for _, __ in self.labels.items()]

    @lazy_property
    def categories(self) -> Set[str]:
        service_categories = \
            _get_service_categories_from_image_labels(self.labels)
        if self.service.get('categories', None):
            service_categories |= self.service['categories']
        if service_categories:
            self.service['categories'] = service_categories
        return service_categories

    @property
    def is_default(self) -> bool:
        return 'bssenv.default' in self.labels.keys()

    @property
    def is_daemon(self) -> bool:
        return self.type == SERVICE_TYPES.DAEMON.value

    @property
    def is_command(self) -> bool:
        return self.type == SERVICE_TYPES.COMMAND.value

    @property
    def is_data_provider(self) -> bool:
        return self.type == SERVICE_TYPES.DATA_PROVIDER.value

    @property
    def is_data_provider_builder(self) -> bool:
        return \
            self.is_data_provider \
            and self.data_provider_type \
            == SERVICE_TYPES.DATA_PROVIDER_BUILD.value

    @property
    def is_data_provider_compressor(self) -> bool:
        return \
            self.is_data_provider \
            and self.data_provider_type \
            == SERVICE_TYPES.DATA_PROVIDER_COMPRESS.value

    @property
    def is_data_provider_restorer(self) -> bool:
        return \
            self.is_data_provider \
            and self.data_provider_type \
            == SERVICE_TYPES.DATA_PROVIDER_RESTORE.value

    @property
    def commands(self) -> Optional[Dict]:
        return self.bssenv.get('commands', None)

    @property
    def command_run_phase(self) -> Optional[str]:
        if self.is_command:
            return self.labels.get('bssenv.command.run_phase', 'on_demand')

    @lazy_property
    def command_default_args(self) -> List[str]:
        return shlex.split(self.labels[
            'bssenv.command.default.args']) \
            if 'bssenv.command.default.args' in self.labels.keys() \
            else []

    @property
    def has_init_command(self) -> bool:
        return 'bssenv.init.service.command' in self.labels.keys()

    @property
    def init_command(self) -> Optional[str]:
        return self.labels.get('bssenv.init.service.command', None)

    @property
    def init_command_type(self) -> Optional[str]:
        if self.has_init_command:
            return self.labels.get(
                'bssenv.init.service.command.type', INIT_TYPES.ALWAYS.value)

    @lazy_property
    def entrypoint_command(self) -> List[str]:
        entrypoint_command = self.composefile_entry.get('command', None)
        return shlex.split(entrypoint_command) \
            if isinstance(entrypoint_command, str) \
            else (
                entrypoint_command
                if isinstance(entrypoint_command, List)
                else [])

    @property
    def command_shell_name(self) -> Optional[str]:
        return self.labels.get('bssenv.command.shell.name', None)

    @lazy_property
    def autocompletion(self) -> Optional[str]:
        if "bssenv.command.bash.autocompletion" in self.labels.keys():
            return self.labels["bssenv.command.bash.autocompletion"] \
                .replace('$$', '$')

    @lazy_property
    def start_dependencies(self) -> Set[str]:
        return \
            set(self.labels['bssenv.start.dependencies'].split(';')) \
            if 'bssenv.start.dependencies' in self.labels.keys() \
            else set()

    @lazy_property
    def start_healthy_dependencies(self) -> Set[str]:
        return \
            set(self.labels['bssenv.start.healthy.dependencies'].split(';')) \
            if 'bssenv.start.healthy.dependencies' in self.labels.keys() \
            else set()

    @lazy_property
    def stop_dependencies(self) -> Set[str]:
        return \
            set(self.labels['bssenv.stop.dependencies'].split(';')) \
            if 'bssenv.stop.dependencies' in self.labels.keys() \
            else set()

    @property
    def image(self) -> Optional[str]:
        return self.composefile_entry.get('image', None)

    @image.setter
    def image(self, image: str) -> None:
        self.composefile_entry['image'] = image

    @property
    def image_sha(self) -> str:
        return self.bssenv['image']['sha']

    @image_sha.setter
    def image_sha(self, image: str) -> None:
        self.bssenv['image']['sha'] = image

    @property
    def image_name(self) -> str:
        return self.bssenv['image']['name']

    @image_name.setter
    def image_name(self, image: str) -> None:
        self.bssenv['image']['name'] = image

    @property
    def image_guard_container(self) -> str:
        return self.bssenv['image']['guard_container']

    @image_guard_container.setter
    def image_guard_container(self, image: str) -> None:
        self.bssenv['image']['guard_container'] = image

    @lazy_property
    def stop_grace_period(self) -> Optional[int]:
        stop_grace_period = self.composefile_entry.get(
            'stop_grace_period', None)
        if stop_grace_period:
            period = stop_grace_period[-1]
            value = stop_grace_period[:-1]
            periods = {
                's': 1,       # seconds
                'm': 60,      # minutes
                'h': 60 * 60  # hours
            }
            stop_grace_period = int(value) * periods[period]
        return stop_grace_period

    @lazy_property
    def container_name(self) -> Optional[str]:
        container_name = self.composefile_entry.get('container_name', None)
        return expandvars(container_name) \
            if container_name is not None else None

    @container_name.setter
    def container_name(self, container_name: str) -> None:
        self.composefile_entry['container_name'] = container_name

    @property
    def logs_path(self) -> Optional[str]:
        return self.labels.get('bssenv.logs.path', None)

    @property
    def data_path(self) -> Optional[str]:
        return self.labels.get('bssenv.data.path', None)

    @property
    def conf_path(self) -> Optional[str]:
        return self.labels.get('bssenv.conf.path', None)

    @property
    def status_name(self) -> str:
        return self.labels.get('bssenv.status.name', self.key)

    @lazy_property
    def ports(self) -> Dict[str, Dict[str, Union[int, None]]]:
        ports = dict()
        for label_key in self.labels.keys():
            if label_key.startswith('bssenv.port.'):
                port_names = set(
                    label_key.replace('bssenv.port.', '').split('.'))
                port_host_default_value, _, port_docker = \
                    self.labels[label_key].rpartition(':')
                port_docker = int(port_docker)
                port_host_default_value = int(port_host_default_value) \
                    if port_host_default_value else port_docker
                port_host = None
                for port_def in self.composefile_entry.get('ports', []):
                    # 9000:9000
                    port_def_host, port_def_docker = port_def.split(':')
                    port_def_docker = int(port_def_docker)
                    if port_docker == port_def_docker:
                        port_host = int(port_def_host)
                        break
                ports = {
                    **ports,
                    **{_: {
                        'host': port_host,
                        'docker': port_docker,
                        'default': port_host_default_value,
                        'names': port_names}
                       for _ in port_names}}
        return ports

    @lazy_property
    def urls(self) -> Dict[str, str]:
        urls = dict()
        for label_key in self.labels.keys():
            if label_key.startswith('bssenv.url.'):
                url_name = label_key.replace('bssenv.url.', '')
                url = self.labels[label_key] \
                    .replace('$${host}', local.os.hostname())
                for port_key, port in self.ports.items():
                    url = url.replace(
                        f'$${{port.{port_key}}}',
                        str(port['host'] or f'${{port.{port_key}}}'))
                urls[url_name] = url
        return urls

    @lazy_property
    def env(self) -> Dict[str, str]:
        env = dict()
        for env_entry in self.composefile_entry.get('environment', []):
            # key=value
            key, _, value = env_entry.partition('=')
            env[key] = value
        return env

    @lazy_property
    def export_files(self) -> Dict[str, str]:
        export_files = dict()
        for label_key in self.labels.keys():
            if label_key.startswith('bssenv.export.file.'):
                file_name = label_key.replace('bssenv.export.file.', '')
                file_path = self.labels[label_key]
                export_files[file_name] = file_path
        return export_files

    @lazy_property
    def network_aliases(self) -> Set[str]:
        network_aliases = {self.key}
        networks = self.composefile_entry.get('networks', None)
        if networks is not None \
                and isinstance(networks, dict) \
                and 'default' in networks.keys():
            for alias in networks['default'].get('aliases', []):
                network_aliases.add(alias)
        return network_aliases

    @property
    def description(self) -> str:
        return self.labels.get('bssenv.description', '')

    @lazy_property
    def switches(self) -> Dict[str, Dict[str, Union[str, None]]]:
        switches = dict()
        for label_key in self.labels.keys():
            if label_key.startswith('bssenv.switch.'):
                *_, switch_name, switch_env_name = label_key.split('.')
                switch_description = self.labels[label_key]
                switches[switch_name] = {
                    'env_name': switch_env_name,
                    'description': switch_description
                }
        return switches
