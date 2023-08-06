# imports from normal python site packages
import sys
from pathlib import Path
from os import PathLike
from typing import List, Tuple
from . import paths, env
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
BSSENV_PKG_DIR = Path(BSSENV_PKG.__file__).resolve().parent
BSSENV_PKG_PYT_SITE_PKGS = BSSENV_PKG_DIR / 'data' / 'python_site_packages'
sys.path = [str(BSSENV_PKG_PYT_SITE_PKGS)] + sys.path

# import from custom site packages
from config import ConfigurationSet, config_from_yaml, config_from_dotenv, config_from_env


def _get_all_configuration_files() -> List[Tuple[str, PathLike, bool]]:
    config_files = []
    for path in reversed(
        [
            paths.BSSENV_PKG_CONFIG_DIR,
            paths.SYSTEM_CONFIG_DIR,
            paths.USER_CONFIG_DIR
        ] + ([] if not env.is_activated() else [paths.ENV_CONFIG_DIR])
    ):
        config_files += path.glob('*.yml')
    return [
        config_from_yaml(str(_.resolve()), True) for _ in config_files]


config = ConfigurationSet(
    *_get_all_configuration_files(),
    # config_from_dotenv(str(paths.ENV_DOT_ENV_FILE), True, lowercase_keys=True),
    config_from_env(prefix='BSSENV', separator='_', lowercase_keys=True)
)
