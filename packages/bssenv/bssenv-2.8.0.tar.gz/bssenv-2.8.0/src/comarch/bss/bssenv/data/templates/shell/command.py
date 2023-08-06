#!/usr/bin/env python3

# imports from normal python site packages
import sys
import traceback
from pathlib import Path
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
LIBS_DIR = SCRIPT_DIR_PATH / '..' / '..' / 'lib' / 'python'
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS), str(LIBS_DIR)] + sys.path

# import from custom site packages
import local.services
from local.logging import speak
from local.paths import ENV_MAIN_LOG_FILE


service_key = '<SERVICE_KEY>'

try:
    cmd_args = sys.argv[1:]
    local.services.start(service_key, wait=False, cmd_args=cmd_args)
except Exception as e:
    if 'returned non-zero exit status' not in str(e):
        trace = traceback.format_exc()
        speak(f'Error during execution of command: "{service_key}". '
              f'Check logs for details: {ENV_MAIN_LOG_FILE}\n\n'
              f'{e}\n'
              f'Traceback:\n'
              f'{trace}')
    else:
        speak(f'Error during execution of command: "{service_key}". '
              f'Check logs for details: {ENV_MAIN_LOG_FILE}')
    exit(1)
