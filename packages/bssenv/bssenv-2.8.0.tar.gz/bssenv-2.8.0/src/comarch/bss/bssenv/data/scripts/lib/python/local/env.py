# imports from normal python site packages
import sys
import os
from pathlib import Path
from . import paths
from . import const
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


_IS_ACTIVATED: bool = None
_NAME: str = None
_ID: str = None
_INSTALL_TYPE: str = None
_VERSION: str = None


def is_activated() -> bool:
    global _IS_ACTIVATED
    global _NAME
    if _IS_ACTIVATED is None:
        if os.environ.get('BSSENV_NAME', None):
            env_name = paths.ENV_DIR.name
            if env_name != 'data':
                _NAME = env_name
            _IS_ACTIVATED = _NAME == os.environ['BSSENV_NAME']
        else:
            _IS_ACTIVATED = False
    return _IS_ACTIVATED


def dir() -> str:
    if is_activated():
        return paths.ENV_DIR


def name() -> str:
    if is_activated():
        return _NAME


def id():
    global _ID
    if is_activated():
        if _ID is None:
            _ID = paths.ENV_DOT_BSSENV_FILE.read_text().strip()
        return _ID


def install_type() -> str:
    global _INSTALL_TYPE
    if is_activated():
        if _INSTALL_TYPE is None:
            _INSTALL_TYPE = paths.BSSENV_INSTALL_TYPE_FILE.read_text().strip()
        return _INSTALL_TYPE


def version() -> str:
    global _VERSION
    if is_activated():
        if _VERSION is None:
            _VERSION = paths.BSSENV_VERSION_FILE.read_text().strip()
        return _VERSION


def get_deleter_image_name() -> str:
    if is_activated():
        return f'{const.BSSENV_DELETER_IMAGE_NAMESPACE}:{id()}'
