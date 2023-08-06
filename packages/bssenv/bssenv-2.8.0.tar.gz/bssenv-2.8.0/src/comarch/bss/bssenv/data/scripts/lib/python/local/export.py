# imports from normal python site packages
import sys
from pathlib import Path
from typing import Union
from local.docker import dockerClient
from local.entities import Service
from local.paths import ENV_TMP_DIR
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


def _export_file_from_container(
        container_name: str,
        file_path: Union[str, Path]) -> str:
    file_container_path = Path(file_path)
    file_name = file_container_path.name
    exported_file_tmp_path = ENV_TMP_DIR / file_name
    dockerClient.export_container_path(
            container_name, file_container_path, ENV_TMP_DIR)
    export_str = exported_file_tmp_path.read_text()
    exported_file_tmp_path.unlink()
    return export_str


def _create_temporary_container(image_sha: str) -> str:
    image = dockerClient.get_image(image_sha)
    return dockerClient.create_container(
            image_sha,
            labels={_: None for _ in image.labels.keys()
                    if _.startswith('com.docker.compose.')})


def export_text_file(service: Service, file_name: str) -> str:
    if not(service.is_data_provider_builder) \
            and file_name in service.export_files.keys():
        file_path = service.export_files[file_name]
        if service.container_name is not None \
                and dockerClient.container_exists(service.container_name):
            return _export_file_from_container(
                service.container_name, file_path)
        else:
            container_name = _create_temporary_container(service.image_sha)
            try:
                export_str = _export_file_from_container(
                    container_name, file_path)
            finally:
                dockerClient.rm_container(container_name)
            return export_str
