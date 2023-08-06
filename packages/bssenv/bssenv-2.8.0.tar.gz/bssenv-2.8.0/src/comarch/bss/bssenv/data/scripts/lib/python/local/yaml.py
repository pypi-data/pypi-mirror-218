# imports from normal python site packages
import sys
import os
from pathlib import Path
from typing import Dict
import yaml
from yaml import Loader
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
LIBS_DIR = SCRIPT_DIR_PATH.parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS), str(LIBS_DIR)] + sys.path

# import from custom site packages


def file_to_dict(path: str) -> Dict:
    with open(path) as f:
        return yaml.load(f, Loader=Loader)


def dict_to_file(a_dict: dict, path: str) -> None:
    with open(path, 'w', encoding='utf8') as f:
        yaml.dump(a_dict, f, default_flow_style=False, allow_unicode=True)


def str_to_dict(a_str: str) -> Dict:
    return yaml.load(a_str, Loader=Loader)


def dict_to_str(a_dict: dict) -> str:
    return yaml.dump(a_dict, default_flow_style=False, allow_unicode=True, sort_keys=False)
