# imports from normal python site packages
import sys
from pathlib import Path
from typing import Union, Any
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


class arg:

    def __getitem__(self, idx: Union[int, slice]) -> Any:
        return sys.argv[idx]

    def __len__(self) -> int:
        return len(sys.argv)

    def __call__(self, idx: int) -> Any:
        if idx == -1:
            arg, = sys.argv[-1:] or [None]
        else:
            arg, = sys.argv[idx:idx + 1] or [None]
        return arg


# make it singletone
arg = arg()


def raise_arg_is_required(arg):
    sys.exit(f'Argument "{arg}" is required. Exit\n')
