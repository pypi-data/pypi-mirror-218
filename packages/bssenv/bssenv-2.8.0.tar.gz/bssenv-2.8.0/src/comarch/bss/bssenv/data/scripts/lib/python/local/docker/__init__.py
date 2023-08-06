import re
import json
from pathlib import Path
from typing import Union, Tuple, Dict
from functools import lru_cache
from ..const import BSSENV_COMPOSEFILE_NAMESPACE, BSSENV_CONFIGMAP_NAMESPACE
from ..logging import debug
from ..entities import SERVICE_TYPES, CONFIG_MAP_TYPES, SimpleService, SimpleConfigMap
from ..config import config

# Type aliases
Entity_key = str
Service_key = str
Image_name = str
Container_name = str
Registry = str
Namespace = str
Repository = str
Tag = str
Image_id = str
Container_id = str
Image_Name_or_Id = Union[Image_id, Image_name]
Container_Name_or_Id = Union[Container_id, Container_name]

# Regexp patterns
REPOSITORY_PART_REGEX = re.compile(r'[a-z0-9]+(?:(?:[a-z0-9]+)*(?:(?<!_)(?<!-)(?<!\.)\.)*(?:(?<!\.)(?<!-)(?<!__)_)*(?:(?<!\.)(?<!_)-)*(?:[a-z0-9]+)*)*(?<!\.)(?<!-)(?<!_)')  # noqa: E501
REPOSITORY_REGEX = re.compile(f'(?:{REPOSITORY_PART_REGEX.pattern}){{1}}(?:/{REPOSITORY_PART_REGEX.pattern})*')
TAG_REGEX = re.compile(r'[_a-zA-Z0-9]+[_\.\-a-zA-Z0-9]*')
REFERENCE_REGEX = re.compile(f'(?:{REPOSITORY_REGEX.pattern}){{1}}:(?:{TAG_REGEX.pattern}){{1}}')
REGISTRY_REGEX = re.compile(r'')  # TODO: uzupelnic


# NAMES >

def split_image_name(image_name: Image_name) -> Tuple[Union[None, Registry], Union[None, Namespace], Repository, Tag]:
    registry, namespace, repository, tag = (None, None, None, None)
    if image_name:
        rest, _, repository_tag = image_name.rpartition('/')
        repository, _, tag = repository_tag.partition(':')
        tag = tag if tag else None
        rest = [_ for _ in rest.split('/') if _]
        if len(rest) > 0 and (
            '.' in rest[0] or
            ':' in rest[0] or
            rest[0] == 'localhost'
        ):
            registry = rest[0]
            rest = rest[1:]
        else:
            registry = None
        if len(rest) > 0:
            namespace = '/'.join(rest)
        else:
            namespace = None
    return (registry, namespace, repository, tag)


def join_image_name_parts(
        registry: Union[None, Registry],
        namespace: Union[None, Namespace],
        repository: Repository,
        tag: Union[None, Tag]) -> Union[None, Image_name]:
    image_name = None
    if repository:
        image_name = repository
        if tag:
            image_name = f'{image_name}:{tag}'
        if namespace:
            image_name = f'{namespace}/{image_name}'
        if registry:
            image_name = f'{registry}/{image_name}'
    return image_name


def entity_image_to_bssenv_descriptor_image(image_name: Image_name) -> Image_name:
    registry, namespace, repository, tag = split_image_name(image_name)
    if namespace and (
        namespace in {BSSENV_COMPOSEFILE_NAMESPACE, BSSENV_CONFIGMAP_NAMESPACE}
        or namespace.endswith(f'/{BSSENV_COMPOSEFILE_NAMESPACE}')
        or namespace.endswith(f'/{BSSENV_CONFIGMAP_NAMESPACE}')
    ):
        # given image is already a descriptor image
        return image_name
    # from this point on, it must already be a service image
    # (because config maps images have the same name as bssenv descriptors
    # images so these should be returned in the previous "if")
    prefix = '/'.join([_ for _ in [registry, namespace, BSSENV_COMPOSEFILE_NAMESPACE, repository] if _ is not None])
    return f'{prefix}:{tag}'


def descriptor_image_to_service_image(image_name: Image_name) -> Image_name:
    if BSSENV_COMPOSEFILE_NAMESPACE in image_name:
        registry, namespace, repository, tag = split_image_name(image_name)
        if namespace == BSSENV_COMPOSEFILE_NAMESPACE:
            namespace = None
        elif namespace.endswith(f'/{BSSENV_COMPOSEFILE_NAMESPACE}'):
            namespace = namespace[0:-(len(BSSENV_COMPOSEFILE_NAMESPACE) + 1)]
        elif namespace.startswith(f'{BSSENV_COMPOSEFILE_NAMESPACE}/'):
            namespace = namespace[len(BSSENV_COMPOSEFILE_NAMESPACE) + 1]
        else:
            namespace = namespace.replace(f'/{BSSENV_COMPOSEFILE_NAMESPACE}/', '/', 1)
        prefix = '/'.join([_ for _ in [registry, namespace, repository] if _ is not None])
        return f'{prefix}:{tag}'

# NAMES <


# REGISTRIES >

def get_registry_name_or_else_default(registry: str = None) -> str:
    return registry if registry else config.repositories.docker.default.registry


# TODO: docelowo nalezy zweryfikowac czy jestesmy w stanie zaimplementowac obsluge wszystkich credentials services
# np. poprzez wykorzystanie https://pypi.org/project/keyring/
# trzeba to przetestowac (różne credentials service + różne systemy operacyjne) i sprawdzić też działanie na
# headless linux (sesja bez GUI) i w dockerze (??? tu nie wiem czy jest sens bo tu wchodzimy w zagadnienie docker
# in docker i chyba nikt nie odpala bssenva w dockerze. Wiec mozna sprawdzic ale jak bedzie czas i okaze sie ze nie
# jest to jakos strasznie trudne)
@lru_cache(maxsize=None)
def get_registry_credentials(registry: str) -> Tuple[str, str]:
    config_path = Path('~/.docker/config.json').expanduser()
    if not config_path.is_file():
        config_path = Path('~/.dockercfg').expanduser()
    if config_path.is_file():
        import base64
        with config_path.open() as f:
            config = json.load(f)
        if credentials_store := config.get('credsStore', None):
            # get authorization data from credentials service
            if credentials_store != 'secretservice':
                raise Exception(f"Credentials service '{credentials_store}' not supported!")
            import secretstorage
            connection = secretstorage.dbus_init()
            collection = secretstorage.get_any_collection(connection)
            item = next(collection.search_items({'label': 'Docker Credentials', 'server': registry}), None)
            if item is None:
                raise Exception(f"Can't find registry credentials in credentials service '{credentials_store}'")
            username = item.get_attributes().get('username', '<token>')
            secret = item.get_secret().decode('utf-8')
            return (username, secret)
        else:
            # get authorization data directly from config file
            registry_config = config.get('auths', {}).get(registry, None)
            if registry_config is None:
                raise Exception(f"Can't find registry credentials for '{registry}' in config file '{config_path}'")
            login_password_base64_string = registry_config['auth']
            login_password_base64_bytes = login_password_base64_string.encode('ascii')
            login_password_bytes = base64.b64decode(login_password_base64_bytes)
            login_password = login_password_bytes.decode('utf-8')
            username, secret = login_password.split(':')
            return (username, secret)
    else:
        raise Exception("Can't find any docker configuration file with credentials entries")


def get_registry_data(registry: str = None) -> Dict:
    try:
        registry = get_registry_name_or_else_default(registry)
        return config.repositories.docker.registries[registry]
    except KeyError:
        return None


def get_remote_name_for_local_image_name(
        image_name: str, registry: str = None) -> str:
    registry = get_registry_name_or_else_default(registry)
    registry_data = get_registry_data(registry)
    port = registry_data.get('port', None)
    remote_image_name = registry
    if port is not None:
        remote_image_name = f'{remote_image_name}:{port}'
    if registry_data.get('docker.image.name.namespace_prefix', None):
        namespace_prefix = registry_data.docker.image.name.namespace_prefix
        if not image_name.startswith(f'{namespace_prefix}/'):
            remote_image_name = f'{remote_image_name}/{namespace_prefix}'
    return f'{remote_image_name}/{image_name}'

# REGISTRIES <


# OTHERS >

# Entity_key:
#   abc -> service
#   :abc -> config map
def descriptor_labels_to_simple_entities_dict(
        labels: Dict) -> Dict[Entity_key, Union[SimpleService, SimpleConfigMap]]:
    entities = dict()
    debug(f'labels: {labels}')
    for key, label_value in labels.items():
        debug(f'descriptor_labels_to_simple_entities_dict.key: {key}')
        debug(f'descriptor_labels_to_simple_entities_dict.value: {label_value}')
        if key.startswith('bssenv.'):
            key = key[7:]
            if key.startswith('service.'):
                entity_key, _, label_key = key[8:].partition('.')
            elif key.startswith('configmap.'):
                entity_key, _, label_key = key[10:].partition('.')
                entity_key = f':{entity_key}'
                if not label_key:
                    # "bssenv.configmap.backend-env-connection_properties": "/config/maps/envs/connection_properties.env"  # noqa: E501
                    label_key = 'path'
            else:
                entity_key, _, label_key = key.partition('.')
            entities[entity_key] = {
                'labels': {
                    **entities.get(entity_key, {}).get('labels', {}),
                    label_key: label_value}}
    for entity_key in entities.keys():
        debug(f'entity_key: {entity_key}')
        if entity_key.startswith(':'):
            # config map
            configmap = SimpleConfigMap()
            configmap.name = entity_key[1:]
            configmap.labels = entities[entity_key]['labels']
            configmap.is_default = 'default' in configmap.labels.keys()
            configmap.cm_tyoe = \
                CONFIG_MAP_TYPES.ENV.value if 'asEnvs' in configmap.labels.keys() else CONFIG_MAP_TYPES.FILE.value
            configmap.path = configmap.labels['path']
            entities[entity_key] = configmap
        else:
            # service
            service = SimpleService()
            service.labels = entities[entity_key]['labels']
            if 'service.types' in service.labels.keys():
                service.types = set(service.labels['service.types'].split(';'))
            else:
                # DEPRECATED
                service.types = set(service.labels['service_type'].split(';'))
            service.is_default = 'default' in service.labels.keys()
            service_name = entity_key
            if \
                    SERVICE_TYPES.DATA_PROVIDER_BUILD.value in service.types \
                    and service_name.endswith('_build'):
                service_name = service_name[0:-6]
            elif \
                    SERVICE_TYPES.DATA_PROVIDER_COMPRESS.value \
                    in service.types \
                    and service_name.endswith('_compress'):
                service_name = service_name[0:-9]
            elif \
                    SERVICE_TYPES.DATA_PROVIDER_RESTORE.value \
                    in service.types \
                    and service_name.endswith('_restore'):
                service_name = service_name[0:-8]
            service.name = service_name
            entities[entity_key] = service
    return entities

# OTHERS <
