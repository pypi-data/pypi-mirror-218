# imports from normal python site packages
import sys
from pathlib import Path
from local.logging import debug
from local.os import exec2
import local.paths
import local.docker
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


BSSENV_GLOBAL_TMP_DIR = local.paths.BSSENV_GLOBAL_TMP_DIR
ENV_DIR = local.paths.ENV_DIR
ENV_TMP_DIR = local.paths.ENV_TMP_DIR


def clean_env_tmp_dir() -> None:
    debug(f'Clean environment temporary directory {ENV_TMP_DIR}')
    try:
        local.os.remove_path(ENV_TMP_DIR)
    except Exception:
        # use docker container because there could be files with root owner
        result = exec2(
            ["docker", "run", "--rm", "-v", f"{ENV_DIR}:/env", "-w", "/env",
             "alpine:latest", "sh", "-c",
             f"rm -rf ./{ENV_TMP_DIR.relative_to(ENV_DIR)}"])
        if result.returncode != 0:
            raise Exception(
                f"Can't delete environment temporary directory:\n"
                f"exit code: {result.returncode}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}")
    local.os.create_dir(ENV_TMP_DIR)
