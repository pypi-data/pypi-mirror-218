# imports from normal python site packages
import sys
from pathlib import Path
from typing import Iterable, Callable
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


def each(iterable: Iterable, callable: Callable, expand: str = None) -> None:
    for item in iterable:
        if expand == 'args':
            callable(*item)
        elif expand == 'kwargs':
            callable(**item)
        else:
            callable(item)
