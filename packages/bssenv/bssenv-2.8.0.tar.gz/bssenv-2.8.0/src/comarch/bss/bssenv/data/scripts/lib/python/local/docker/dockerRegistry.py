# imports from normal python site packages
import os
import sys
import json
import io
import threading
import time
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from urllib.parse import urlparse, urlunparse, quote_plus
from pathlib import Path
from typing import List, Dict, Union, Set, Tuple, Iterator, Optional
from . import (
    Entity_key, Repository, Tag,
    dockerClient, descriptor_image_to_service_image, entity_image_to_bssenv_descriptor_image,
    descriptor_labels_to_simple_entities_dict, split_image_name, join_image_name_parts,
    get_registry_name_or_else_default, get_registry_data, get_registry_credentials
)
from .. import paths
from .. import env
from ..config import config
from ..logging import debug
from ..entities import ENTITY_TYPES, SimpleService, SimpleConfigMap
from ..threading import register_cancellable, unregister_cancellable
from ..itertools import each
from ..const import \
    BSSENV_NAMESPACE, BSSENV_COMPOSEFILE_NAMESPACE, BSSENV_CONFIGMAP_NAMESPACE
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / 'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages
import requests
from wcmatch import fnmatch


os.environ['REQUESTS_CA_BUNDLE'] = str(paths.BSSENV_PKG_CERTIFICATES_DIR)


class METHOD:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    PATCH = 'PATCH'


class MEDIA_TYPES:
    MANIFEST = 'application/vnd.docker.distribution.manifest.v2+json'
    MANIFEST_LIST = 'application/vnd.docker.distribution.manifest.list.v2+json'
    IMAGE = 'application/vnd.docker.container.image.v1+json'


def _raise_if_error(response: requests.Response) -> None:
    if not response.ok:
        raise requests.exceptions.HTTPError(
            f'{response.status_code} Client Error\n'
            f'response text:\n'
            f'{response.text}'
        )


def _nexus_paginated_request_iterator(
        type: str,
        url: str,
        auth: Tuple[str, str] = None,
        headers: Dict[str, str] = {}
) -> Iterator[str]:
    type = type.upper()
    do_request = \
        requests.get if type == METHOD.GET else \
        requests.post if type == METHOD.POST else \
        requests.put if type == METHOD.PUT else \
        requests.delete if type == METHOD.DELETE else \
        requests.patch if type == METHOD.PATCH else \
        requests.head if type == METHOD.HEAD else None
    if do_request is not None:
        parsed_url = urlparse(url)
        current_url = url
        future = None
        cancel = register_cancellable()
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                while True:
                    if cancel.is_set():
                        return
                    if future is not None:
                        result = future.result()
                        _raise_if_error(result)
                        current_url = None
                        if 'Content-Type' in result.headers \
                                and result.headers['Content-Type'] == 'application/json':
                            json_result = result.json() or {}
                            if 'continuationToken' in json_result.keys() \
                                    and json_result['continuationToken'] is not None:
                                continuation_token = json_result['continuationToken']
                                current_url = urlunparse([
                                    parsed_url.scheme,
                                    parsed_url.netloc,
                                    parsed_url.path,
                                    parsed_url.params,
                                    (
                                        f'{parsed_url.query}&continuationToken={continuation_token}' if parsed_url.query
                                        else f'continuationToken={continuation_token}'
                                    ),
                                    parsed_url.fragment
                                ])
                    else:
                        result = None
                    if current_url is not None:
                        future = executor.submit(
                            do_request,
                            current_url,
                            auth=auth,
                            headers=headers,
                            verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR)
                        )
                    if result is not None:
                        yield result.text
                    if current_url is None:
                        break
        finally:
            unregister_cancellable(cancel)


def _nexus_paginated_request(
        type: str,
        url: str,
        auth: Tuple[str, str],
        headers: Dict[str, str]) -> List[str]:
    return list(*_nexus_paginated_request_iterator(type=type, url=url, auth=auth, headers=headers))


def _docker_paginated_request_iterator(
        type: str,
        url: str,
        auth: Tuple[str, str] = None,
        headers: Dict[str, str] = {},
        n: int = None
) -> Iterator[str]:
    type = type.upper()
    do_request = \
        requests.get if type == METHOD.GET else \
        requests.post if type == METHOD.POST else \
        requests.put if type == METHOD.PUT else \
        requests.delete if type == METHOD.DELETE else \
        requests.patch if type == METHOD.PATCH else \
        requests.head if type == METHOD.HEAD else None
    if do_request is not None:
        parsed_url = urlparse(url)
        v1_request = '/v1/' in parsed_url.path
        current_url = url
        if n is not None:
            current_url = f'{current_url}?n={n}'
        next_page = 0
        current_num_results = 0
        future = None
        cancel = register_cancellable()
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                while True:
                    if cancel.is_set():
                        return
                    if future is not None:
                        result = future.result()
                        _raise_if_error(result)
                        current_url = None
                        if 'next' in result.links:
                            # v2
                            parsed_next_url = urlparse(result.links["next"]["url"])
                            scheme = parsed_next_url.scheme or parsed_url.scheme
                            netloc = parsed_next_url.netloc or parsed_url.netloc
                            path = parsed_next_url.path
                            params = parsed_next_url.params
                            query = parsed_next_url.query
                            fragment = parsed_next_url.fragment
                            current_url = urlunparse([scheme, netloc, path, params, query, fragment])
                        elif v1_request:
                            if 'Content-Type' in result.headers \
                                    and result.headers['Content-Type'] == 'application/json':
                                json_result = result.json() or {}
                                if 'num_pages' in json_result.keys() and 'page' in json_result.keys():
                                    # v1
                                    page = int(json_result['page'])
                                    next_page = page + 1
                                    num_pages = int(json_result['num_pages'])
                                    num_results = int(json_result['num_results'])
                                    page_size = int(json_result['page_size'])
                                    current_num_results += page_size
                                    if current_num_results < num_results and next_page < num_pages:
                                        current_url = urlunparse([
                                            parsed_url.scheme,
                                            parsed_url.netloc,
                                            parsed_url.path,
                                            parsed_url.params,
                                            (
                                                f'{parsed_url.query}&page={next_page}' if parsed_url.query else
                                                f'page={next_page}'
                                            ),
                                            parsed_url.fragment
                                        ])
                    else:
                        result = None
                    if current_url is not None:
                        future = executor.submit(
                            do_request,
                            current_url,
                            auth=auth,
                            headers=headers,
                            verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR)
                        )
                    if result is not None:
                        yield result.text
                    if current_url is None:
                        break
        finally:
            unregister_cancellable(cancel)


def _docker_paginated_request(
        type: str,
        url: str,
        auth: Tuple[str, str],
        headers: Dict[str, str],
        n: int = None) -> List[str]:
    return list(*_docker_paginated_request_iterator(type=type, url=url, auth=auth, headers=headers, n=n))


def get_docker_api_url_for_registry(registry: str = None, api_version='v2') -> str:
    registry = get_registry_name_or_else_default(registry)
    registry_data = get_registry_data(registry)
    port = registry_data.get('port', None)
    scheme = registry_data.get('url.scheme', 'https')
    path_prefix = \
        registry_data.get('docker.api.url.path_prefix', None) or registry_data.get('api.url.path_prefix', None)
    if (
        (
            api_version == 'v2'
            and not registry_data.get('docker.api.v2', False))
        or (
            api_version == 'v1'
            and not registry_data.get('docker.api.v1', False))
    ):
        raise Exception(f'Api version "{api_version}" unavailable for given docker registry "{registry}"')
    url = f'{scheme}://{registry}'
    if port:
        url = f'{url}:{port}'
    if path_prefix:
        url = f'{url}/{path_prefix}'
    return f'{url}/{api_version}'


def get_nexus_api_url_for_registry(registry: str = None, api_version='v1') -> str:
    registry = get_registry_name_or_else_default(registry)
    registry_data = get_registry_data(registry)
    port = registry_data.get('port', None)
    scheme = registry_data.get('url.scheme', 'https')
    if (
            api_version == 'v1'
            and not registry_data.get('nexus.api.v1', False)
    ):
        raise Exception(f'Api version "{api_version}" unavailable for given nexus registry "{registry}"')
    url = f'{scheme}://{registry}'
    if port:
        url = f'{url}:{port}'
    return f'{url}/service/rest/{api_version}'


def _get_all_request_data_for_registry(registry: str = None) -> Tuple[str, str, Dict, Tuple, Dict]:
    registry = get_registry_name_or_else_default(registry)
    registry_data = get_registry_data(registry)
    type = registry_data['type']
    headers = registry_data.as_attrdict().get('request', {}).get('headers', {})
    auth = get_registry_credentials(registry) if registry_data.get('secured', False) else None
    return (type, registry, registry_data, auth, headers)


def repositories_chunked_iterator(registry: str = None) -> Iterator[List[str]]:
    type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
    registry_api_url = get_docker_api_url_for_registry(registry, api_version='v2')
    url = f'{registry_api_url}/_catalog'
    for result in _docker_paginated_request_iterator(METHOD.GET, url, auth=auth, headers=headers, n=500):
        repositories = json.loads(result).get('repositories', []) or []
        yield repositories


def repositories_iterator(registry: str = None) -> Iterator[str]:
    for chunk in repositories_chunked_iterator(registry):
        for repository in chunk:
            yield repository


def repositories(registry: str = None) -> Set[str]:
    repositories = set()
    for chunk in repositories_chunked_iterator(registry):
        repositories.update(chunk)
    return repositories


def repository_tags_chunked_iterator(
        repository: str, registry: str = None) -> Iterator[List[str]]:
    type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
    registry_api_url = get_docker_api_url_for_registry(registry, api_version='v2')
    url = f'{registry_api_url}/{repository}/tags/list'
    try:
        for result in _docker_paginated_request_iterator(METHOD.GET, url, auth=auth, headers=headers, n=10000):
            if result:
                tags = json.loads(result).get('tags', []) or []
                yield tags
    except requests.exceptions.HTTPError as exc:
        if not ('404 Client Error' in str(exc) and "repository name not known to registry" in str(exc)):
            raise exc


def repository_tags_iterator(repository: str, registry: str = None) -> Iterator[str]:
    for chunk in repository_tags_chunked_iterator(repository, registry):
        for tag in chunk:
            yield tag


def repository_tags(repository: str, registry: str = None) -> Set[str]:
    tags = set()
    for chunk in repository_tags_chunked_iterator(repository, registry):
        tags.update(chunk)
    return tags


def _get_image_reference(repository: str, tag: str, namespace: str = None, registry: str = None) -> str:
    registry = get_registry_name_or_else_default(registry)
    registry_data = get_registry_data(registry)
    port = registry_data.get('port', None)
    reference = f'{registry}'
    if port:
        reference = f'{reference}:{port}'
    if namespace:
        reference = f'{reference}/{namespace}'
    return f'{reference}/{repository}:{tag}'


def _repository_tags_chunked_queue_iterator(queue: Queue, repository: str, registry: str = None) -> None:
    for chunk in repository_tags_chunked_iterator(repository, registry):
        queue.put((repository, chunk))
    queue.put((repository, None))


def search_by_tag_iterator(tag_glob: str, registry: str = None) -> Iterator[str]:
    type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
    if type == 'nexus':
        tag_glob = quote_plus(tag_glob)
        registry_api_url = get_nexus_api_url_for_registry(registry, api_version='v1')
        url = f'{registry_api_url}/search?format=docker&docker.imageTag={tag_glob}'
        if registry_data.get('nexus.repository', None):
            url = f'{url}&repository={registry_data.nexus.repository}'
        for _ in _nexus_paginated_request_iterator(METHOD.GET, url, auth=auth, headers=headers):
            items = json.loads(_).get('items', []) or []
            for item in items:
                yield f'{item["name"]}:{item["version"]}'
    elif type == 'docker':
        results = Queue()
        wait_for_number_of_repo_results = 0
        futures = []
        with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
            for repository in repositories_iterator(registry=registry):
                wait_for_number_of_repo_results += 1
                futures.append(e.submit(_repository_tags_chunked_queue_iterator, results, repository, registry))
            while wait_for_number_of_repo_results > 0:
                repository, tags = results.get(timeout=config.timeout.http.default)
                results.task_done()
                if tags is None:
                    wait_for_number_of_repo_results -= 1
                else:
                    for tag in fnmatch.filter(tags, tag_glob):
                        reference = _get_image_reference(repository, tag, registry=registry)
                        yield reference
        for future in futures:
            future.result()


def search_by_tag(tag_glob: str, registry: str = None) -> Set[str]:
    return set([*search_by_tag_iterator(tag_glob=tag_glob, registry=registry)])


def search_by_repository_iterator(repository_glob: str, registry: str = None) -> Iterator[str]:
    type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
    if type == 'nexus':
        repository_glob = quote_plus(repository_glob)
        registry_api_url = get_nexus_api_url_for_registry(registry, api_version='v1')
        url = f'{registry_api_url}/search?format=docker&docker.imageName={repository_glob}'
        if registry_data.get('nexus.repository', None):
            url = f'{url}&repository={registry_data.nexus.repository}'
        for _ in _nexus_paginated_request_iterator(METHOD.GET, url, auth=auth, headers=headers):
            items = json.loads(_).get('items', []) or []
            for item in items:
                yield f'{item["name"]}:{item["version"]}'
    elif type == 'docker':
        results = Queue()
        wait_for_number_of_repo_results = 0
        futures = []
        with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
            for repository in repositories_iterator(registry=registry):
                if fnmatch.fnmatch(repository, repository_glob):
                    wait_for_number_of_repo_results += 1
                    futures.append(e.submit(_repository_tags_chunked_queue_iterator, results, repository, registry))
            while wait_for_number_of_repo_results > 0:
                repository, tags = results.get(timeout=config.timeout.http.default)
                results.task_done()
                if tags is None:
                    wait_for_number_of_repo_results -= 1
                else:
                    for tag in tags:
                        reference = _get_image_reference(repository, tag, registry=registry)
                        yield reference
        for future in futures:
            future.result()


def search_by_repository(repository_glob: str, registry: str = None) -> Set[str]:
    return set([*search_by_repository_iterator(repository_glob=repository_glob, registry=registry)])


def search_by_repository_and_tag_iterator(
        repository_glob: str, tag_glob: str,
        registry: str = None,
        force_docker_api: bool = False) -> Iterator[str]:
    type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
    if not force_docker_api and type == 'nexus':
        quoted_repository_glob = quote_plus(repository_glob)
        quoted_tag_glob = quote_plus(tag_glob)
        registry_api_url = get_nexus_api_url_for_registry(registry, api_version='v1')
        url = \
            f'{registry_api_url}/search?format=docker&docker.imageName={quoted_repository_glob}&docker.imageTag={quoted_tag_glob}'  # noqa: E501
        if registry_data.get('nexus.repository', None):
            quoted_nexus_repository = quote_plus(registry_data.nexus.repository)
            url = f'{url}&repository={quoted_nexus_repository}'
        for _ in _nexus_paginated_request_iterator(METHOD.GET, url, auth=auth, headers=headers):
            items = json.loads(_).get('items', []) or []
            for item in items:
                repository = item["name"]
                tag = item["version"]
                if fnmatch.fnmatch(repository, repository_glob) and fnmatch.fnmatch(tag, tag_glob):
                    reference = _get_image_reference(repository, tag, registry=registry)
                    yield reference
    elif force_docker_api or type == 'docker':
        results = Queue()
        wait_for_number_of_repo_results = 0
        futures = []
        with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
            for repository in repositories_iterator(registry=registry):
                if fnmatch.fnmatch(repository, repository_glob):
                    wait_for_number_of_repo_results += 1
                    futures.append(e.submit(_repository_tags_chunked_queue_iterator, results, repository, registry))
            while wait_for_number_of_repo_results > 0:
                repository, tags = results.get(timeout=config.timeout.http.default)
                results.task_done()
                if tags is None:
                    wait_for_number_of_repo_results -= 1
                else:
                    for tag in fnmatch.filter(tags, tag_glob):
                        reference = _get_image_reference(repository, tag, registry=registry)
                        yield reference
        for future in futures:
            future.result()


def search_by_repository_and_tag(repository_glob: str, tag_glob: str, registry: str = None) -> Set[str]:
    return set(
        [*search_by_repository_and_tag_iterator(repository_glob=repository_glob, tag_glob=tag_glob, registry=registry)])


def image_exists(image_name: str) -> bool:
    registry, namespace, repository, tag = split_image_name(image_name)
    if registry:
        registry = registry.split(':', 1)[0]
        repository = join_image_name_parts(None, namespace, repository, None)
        type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
        headers = {**headers, 'Accept': MEDIA_TYPES.MANIFEST}
        registry_api_url = get_docker_api_url_for_registry(registry, api_version='v2')
        api_url = f'{registry_api_url}/{repository}/manifests/{tag}'
        # print(api_url)
        r = requests.head(api_url, auth=auth, headers=headers, verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR))
        if r.status_code == 404:
            return False
        elif r.status_code == 200:
            return True
        else:
            _raise_if_error(r)
    return False


def get_image_manifest(image_name: str) -> Optional[Dict]:
    registry, namespace, repository, tag = split_image_name(image_name)
    if registry:
        registry = registry.split(':', 1)[0]
        repository = join_image_name_parts(None, namespace, repository, None)
        type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
        headers = {**headers, 'Accept': MEDIA_TYPES.MANIFEST}
        registry_api_url = get_docker_api_url_for_registry(registry, api_version='v2')
        api_url = f'{registry_api_url}/{repository}/manifests/{tag}'
        r = requests.get(api_url, auth=auth, headers=headers, verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR))
        _raise_if_error(r)
        return r.json()


def get_image_manifest_digest(image_name: str) -> Optional[Dict]:
    registry, namespace, repository, tag = split_image_name(image_name)
    if registry:
        registry = registry.split(':', 1)[0]
        repository = join_image_name_parts(None, namespace, repository, None)
        type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
        headers = {**headers, 'Accept': MEDIA_TYPES.MANIFEST}
        registry_api_url = get_docker_api_url_for_registry(registry, api_version='v2')
        api_url = f'{registry_api_url}/{repository}/manifests/{tag}'
        r = requests.head(api_url, auth=auth, headers=headers, verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR))
        _raise_if_error(r)
        return r.headers['Docker-Content-Digest']


def get_image_manifest_config(image_name: str) -> Optional[Dict]:
    manifest = get_image_manifest(image_name)
    if manifest is not None:
        media_type = manifest.get('config', {}).get('mediaType', None)
        if media_type == MEDIA_TYPES.IMAGE:
            registry, namespace, repository, tag = split_image_name(image_name)
            registry = registry.split(':', 1)[0]
            repository = join_image_name_parts(None, namespace, repository, None)
            type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
            registry_api_url = get_docker_api_url_for_registry(registry, api_version='v2')
            digest = manifest['config']['digest']
            api_url = f'{registry_api_url}/{repository}/blobs/{digest}'
            r = requests.get(api_url, auth=auth, headers=headers, verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR))
            _raise_if_error(r)
            return r.json()


def remove_image_manifest(
        digest: str, repository: str, registry: str = None) -> None:
    # this deletes manifest and all tags pinned to it from given repository
    # backend:
    #   tagA -> manifestX
    #   tagB -> manifestX
    #   tagC -> manifestY
    # remove_image_manifest(manifestX, backend) - deletes manifestX
    # and tag A and B from repository backend
    type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
    registry_api_url = get_docker_api_url_for_registry(registry, api_version='v2')
    api_url = f'{registry_api_url}/{repository}/manifests/{digest}'
    # print(api_url)
    r = requests.delete(api_url, auth=auth, headers=headers, verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR))
    debug(str(r))
    if r.status_code == 404:
        # manifest not found so just skip
        return
    _raise_if_error(r)


def get_image_labels(image_name: str) -> Optional[Dict[str, str]]:
    image_config = get_image_manifest_config(image_name)
    if image_config is not None:
        return image_config.get('config', {}).get('Labels', {})


def get_image_tags(image_name: str) -> Optional[Set[str]]:
    registry, namespace, repository, tag = split_image_name(image_name)
    if registry:
        registry = registry.split(':', 1)[0]
        repository = join_image_name_parts(None, namespace, repository, None)
        return repository_tags(repository, registry)


def _nexus_get_component(
        name: str, version: str, nexus_repository: str = None,
        registry: str = None) -> Optional[Dict]:
    type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
    name = quote_plus(name)
    version = quote_plus(version)
    registry_api_url = get_nexus_api_url_for_registry(registry, api_version='v1')
    url = f'{registry_api_url}/search?format=docker&name={name}&version={version}'
    if nexus_repository:
        nexus_repository = quote_plus(nexus_repository)
        url = f'{url}&repository={nexus_repository}'
    r = requests.get(url, auth=auth, headers=headers, verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR))
    _raise_if_error(r)
    items = r.json()['items']
    if items:
        return items[0]
    else:
        return


def _prepare_deleter_image(deleter_image_name: str) -> None:
    response = [line for line in dockerClient.build_image(
        fileobj=io.BytesIO('FROM scratch'.encode('utf-8')),
        tag=deleter_image_name,
        rm=True,
        forcerm=True,
        labels={'description': deleter_image_name})]
    debug(f'response: {response}')


def _wait_until_blob_present_in_repository(
        repository: str, blob_digest: str, cancel: threading.Event, registry: str = None,
        timeout: int = 20) -> None:
    # let's try to avoid error:
    # err.code="manifest blob unknown"
    # so wait max timeout seconds untill docker registry finds out
    # that the given blob is really present in the given repository
    type, registry, registry_data, auth, headers = \
        _get_all_request_data_for_registry(registry)
    registry_api_url = get_docker_api_url_for_registry(registry, api_version='v2')
    api_url = f'{registry_api_url}/{repository}/blobs/{blob_digest}'
    count = 0
    while not cancel.is_set():
        count += 1
        if count > timeout:
            raise Exception(f'Blob "{blob_digest}" not found in docker registry repository: {registry}/{repository}')
        debug(f'Checking existance of blob: {blob_digest}')
        r = requests.head(api_url, auth=auth, headers=headers, verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR))
        if r.ok:
            debug('Blob exists in docker registry repository')
            break
        time.sleep(1)


def tag_image(image_name: str, new_image_name: str) -> None:
    registry, namespace, repository, tag = split_image_name(image_name)
    if registry:
        new_registry, new_namespace, new_repository, new_tag = split_image_name(new_image_name)
        registry = registry.split(':')[0]
        new_registry = new_registry.split(':')[0]
        if registry != new_registry:
            raise Exception('Can only tag images in the same docker registry')
        repository = join_image_name_parts(None, namespace, repository, None)
        new_repository = join_image_name_parts(None, new_namespace, new_repository, None)
        if repository != new_repository:
            cancel = register_cancellable()
            try:
                type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
                registry_api_url = get_docker_api_url_for_registry(registry, api_version='v2')
                manifest = get_image_manifest(image_name)
                # layers
                debug(f'Set all layers to new repo: {new_repository}')
                futures = []
                with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
                    for layer in manifest['layers']:
                        futures.append(e.submit(
                            lambda digest:
                            requests.post(
                                f'{registry_api_url}/{new_repository}/blobs/uploads/?mount={digest}&from={repository}',
                                auth=auth, headers=headers, verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR)),
                            layer["digest"])
                        )
                    each(as_completed(futures), lambda _: _raise_if_error(_.result()))
                futures = []
                with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
                    for layer in manifest['layers']:
                        futures.append(e.submit(
                            lambda digest:
                            _wait_until_blob_present_in_repository(new_repository, digest, cancel, registry),
                            layer["digest"]
                        ))
                    each(as_completed(futures), lambda _: _.result())
                # config
                debug('Set config to new repo')
                r = requests.post(
                    f'{registry_api_url}/{new_repository}/blobs/uploads/?mount={manifest["config"]["digest"]}&from={repository}',  # noqa: E501
                    auth=auth, headers=headers,
                    verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR))
                _raise_if_error(r)
                _wait_until_blob_present_in_repository(new_repository, manifest["config"]["digest"], cancel, registry)
            except Exception as e:
                cancel.set()
                raise e
            finally:
                unregister_cancellable(cancel)
        # manifest
        debug('Set manifest to new repo')
        r = requests.put(
            f'{registry_api_url}/{new_repository}/manifests/{new_tag}',
            headers={
                **headers,
                'content-type':
                'application/vnd.docker.distribution.manifest.v2+json'},
            data=json.dumps(manifest))
        _raise_if_error(r)


def remove_image(image_name: str) -> None:
    registry, namespace, repository, tag = split_image_name(image_name)
    if registry:
        if not tag:
            raise Exception(f'Please provide full image name with tag: {image_name}')
        registry, port, *_ = registry.split(':', 1) + [None]
        repository = join_image_name_parts(None, namespace, repository, None)
        type, registry, registry_data, auth, headers = _get_all_request_data_for_registry(registry)
        if type == 'nexus':
            nexus_repository = registry_data.get('nexus.repository', None)
            component = _nexus_get_component(
                name=repository, version=tag, nexus_repository=nexus_repository, registry=registry)
            if component:
                component_id = component['id']
                registry_api_url = get_nexus_api_url_for_registry(registry, api_version='v1')
                url = f'{registry_api_url}/components/{component_id}'
                # print(url)
                r = requests.delete(url, auth=auth, headers=headers, verify=str(paths.BSSENV_PKG_CERTIFICATES_DIR))
                _raise_if_error(r)
        elif type == 'docker':
            # Caution: this probably should be synchronized if used from
            # multiple threads because deleter docker image is one per whole
            # environment and so deleting multiple environment images in
            # parallel can cause some kind of race condition on deleter image
            # access
            # TODO: taking above into consideration we should create here
            # individual deleter image per each image requested to delete
            deleter_image_name = env.get_deleter_image_name()
            remote_deleter_image_name = registry
            if port is not None:
                remote_deleter_image_name = f'{remote_deleter_image_name}:{port}'
            if registry_data.get('docker.image.name.namespace_prefix', None):
                remote_deleter_image_name = \
                    f'{remote_deleter_image_name}/{registry_data.docker.image.name.namespace_prefix}'
            remote_deleter_image_name = f'{remote_deleter_image_name}/{deleter_image_name}'
            if not image_exists(remote_deleter_image_name):
                if not dockerClient.image_exists(deleter_image_name):
                    _prepare_deleter_image(deleter_image_name)
                dockerClient.tag_image(deleter_image_name, remote_deleter_image_name)
                dockerClient.push_image(remote_deleter_image_name)
            # pin tag from an old image to this deletable image object
            tag_image(remote_deleter_image_name, image_name)
            # remove deletable image from the repository with all tags
            # pinned to it
            manifest_digest = get_image_manifest_digest(image_name)
            debug(f'manifest_digest: {manifest_digest}')
            remove_image_manifest(manifest_digest, repository, registry)


# Entity_key:
#   abc -> service
#   :abc -> config map
def get_config_maps_for_image(image: str) -> Dict[Entity_key, SimpleConfigMap]:
    config_maps = dict()
    entities = dict()
    try:
        labels = get_image_labels(image)
        if labels is not None:
            debug(f'dr.get_config_maps_for_image.labels: {labels}')
            entities = descriptor_labels_to_simple_entities_dict(labels)
            for entity_key, entity in entities.items():
                if entity.type == ENTITY_TYPES.CONFIGMAP.value:
                    entity.image = image
                    entity.descriptor_image = image  # config maps images are descriptors images themselves
                    config_maps[entity_key] = entity
    except Exception as exc:
        debug(f'dr.get_config_maps_for_image.exc: {exc}')
        return dict()
    return config_maps


# Entity_key:
#   abc -> service
#   :abc -> config map
def get_services_for_descriptor_image(descriptor_image: str) -> Dict[Entity_key, SimpleService]:
    services = dict()
    entities = dict()
    try:
        service_image = descriptor_image_to_service_image(descriptor_image)
        labels = get_image_labels(descriptor_image)
        if labels is not None:
            debug(f'dr.get_services_for_descriptor_image.labels: {labels}')
            entities = descriptor_labels_to_simple_entities_dict(labels)
            for entity_key, entity in entities.items():
                if entity.type == ENTITY_TYPES.SERVICE.value:
                    entity.image = service_image
                    entity.descriptor_image = descriptor_image
                    services[entity_key] = entity
    except Exception as exc:
        debug(f'dr.get_services_for_descriptor_image.exc: {exc}')
        return dict()
    return services


# Entity_key:
#   abc -> service
#   :abc -> config map
def get_services_for_image(image: str) -> Dict[Entity_key, SimpleService]:
    return get_services_for_descriptor_image(entity_image_to_bssenv_descriptor_image(image))


# Entity_key:
#   abc -> service
#   :abc -> config map
def get_entities_for_tag(
        tag: str,
        namespace: Union[None, str] = None,
        registry: str = None) -> Dict[Entity_key, Union[SimpleService, SimpleConfigMap]]:
    _, registry, registry_data, _, _ = _get_all_request_data_for_registry(registry)
    if namespace is not None:
        namespace = f'{namespace}/{BSSENV_NAMESPACE}'
    else:
        namespace = BSSENV_NAMESPACE
    namespace_prefix = registry_data.get('docker.image.name.namespace_prefix', None)
    if namespace_prefix and not namespace.startswith(f'{namespace_prefix}/'):
        namespace = f'{namespace_prefix}/{namespace}'
    debug(f'get_entities_for_tag.namespace: {namespace}')
    escaped_namespace = glob.escape(namespace)
    escaped_tag = glob.escape(tag)
    entities = dict()
    futures = []
    with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
        for image in search_by_repository_and_tag_iterator(
                repository_glob=f'{escaped_namespace}/*/*', tag_glob=escaped_tag, registry=registry):
            _, img_namespace, _, img_tag = split_image_name(image)
            if img_tag == tag:
                if img_namespace == f'{namespace}/composefile':
                    futures.append(e.submit(get_services_for_descriptor_image, image))
                elif img_namespace == f'{namespace}/configmap':
                    futures.append(e.submit(get_config_maps_for_image, image))
        for future in as_completed(futures):
            entities.update(future.result())
    return entities


def get_all_bssenv_descriptors_tags() -> Dict[Repository, Set[Tag]]:
    all_tags = dict()
    futures = []
    with ThreadPoolExecutor(max_workers=config.thread.pool.max.workers) as e:
        for repository in repositories_iterator():
            _, namespace, *_ = split_image_name(repository)
            if namespace is not None \
                    and (
                        namespace == BSSENV_COMPOSEFILE_NAMESPACE
                        or namespace.endswith(f'/{BSSENV_COMPOSEFILE_NAMESPACE}')
                        or namespace == BSSENV_CONFIGMAP_NAMESPACE
                        or namespace.endswith(f'/{BSSENV_CONFIGMAP_NAMESPACE}')
                    ):
                futures.append(e.submit(lambda _: (_, repository_tags(_)), repository))
        for future in as_completed(futures):
            repository, tags = future.result()
            all_tags[repository] = tags
    return all_tags


def get_image_size(image_name: str) -> Optional[int]:
    manifest = get_image_manifest(image_name)
    if manifest is not None:
        return sum(_['size'] for _ in manifest.get('layers', []))


def get_image_virtual_size(image_name: str) -> Optional[int]:
    return get_image_size(image_name)
