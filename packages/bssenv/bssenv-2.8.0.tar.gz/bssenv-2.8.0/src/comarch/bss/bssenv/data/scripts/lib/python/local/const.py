# imports from normal python site packages
import sys
import os
from pathlib import Path
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


# TODO: czy nie powinno sie tez dac ustawiac w configu?
# i w ogole to chyba nie jest const i powinno raczej wyleciec do tego pliku:
# src/comarch/bss/bssenv/data/scripts/lib/python/local/docker/__init__.py
BSSENV_DOCKER_NETWORK_MTU = int(os.environ.get('BSSENV_DOCKER_NETWORK_MTU', 1500))

BSSENV_NAMESPACE = 'bssenv'
BSSENV_COMPOSEFILE_NAMESPACE = 'bssenv/composefile'
BSSENV_CONFIGMAP_NAMESPACE = 'bssenv/configmap'
BSSENV_SNAPSHOT_NAMESPACE = 'snapshot'
BSSENV_DELETER_IMAGE_NAMESPACE = 'bssenv/deleter/image'
