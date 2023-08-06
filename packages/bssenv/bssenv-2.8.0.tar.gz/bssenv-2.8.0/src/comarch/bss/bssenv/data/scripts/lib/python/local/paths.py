# imports from normal python site packages
import sys
import os
import tempfile
from pathlib import Path
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR = Path(__file__).resolve().parent
LIBS_DIR = SCRIPT_DIR.parent
BSSENV_PKG_DIR = Path(BSSENV_PKG.__file__).resolve().parent
BSSENV_PKG_PYT_SITE_PKGS = BSSENV_PKG_DIR / 'data' / 'python_site_packages'
sys.path = [str(BSSENV_PKG_PYT_SITE_PKGS), str(LIBS_DIR)] + sys.path

# import from custom site packages


BSSENV_PKG_DATA_DIR = BSSENV_PKG_DIR / 'data'
BSSENV_PKG_INTERNAL_DIR = BSSENV_PKG_DIR / 'internal'
BSSENV_PKG_CERTIFICATES_DIR = BSSENV_PKG_DATA_DIR / 'certificates'

ENV_DIR = (SCRIPT_DIR / '..' / '..' / '..' / '..').resolve()
ENV_DOT_ENV_FILE = ENV_DIR / '.env'
ENV_DOT_BSSENV_FILE = ENV_DIR / '.bssenv'
ENV_DOT_VENV_DIR = ENV_DIR / '.venv'
ENV_DOCKER_DIR = ENV_DIR / 'docker'
ENV_PML_DIR = ENV_DIR / 'PML'
ENV_CONFIG_MAPS_DIR = ENV_DIR / 'config_maps'

# CONFIGS
BSSENV_PKG_CONFIG_DIR = BSSENV_PKG_INTERNAL_DIR / 'config'  # config 1: at bssenv package level  # noqa: E501
SYSTEM_CONFIG_DIR = Path('/var/bssenv')  # config 2: at system level
USER_CONFIG_DIR = Path('~/.local/share/bssenv').expanduser()  # config 3: at user level  # noqa: E501
ENV_CONFIG_DIR = ENV_DIR / 'config'  # config 4: at current environment level

# LOGS
ENV_LOGS_DIR = ENV_DIR / 'logs'
ENV_MAIN_LOG_FILE = ENV_LOGS_DIR / 'bssenv.log'

# TEMPORARY DIRECTORIES
BSSENV_GLOBAL_TMP_DIR = Path(
    os.environ.get('BSSENV_GLOBAL_TMP_DIR', tempfile.gettempdir()))
ENV_TMP_DIR = ENV_DIR / '.tmp'

ENV_BIN_DIR = ENV_DOT_VENV_DIR / 'bin'
ENV_BIN2_DIR = ENV_DOT_VENV_DIR / 'bin2'
ENV_LIB_DIR = ENV_DOT_VENV_DIR / 'lib'
ENV_AUTOCOMPLETION_DIR = ENV_DOT_VENV_DIR / 'autocompletion'
ENV_TEMPLATES_DIR = ENV_DOT_VENV_DIR / 'templates'
ENV_VAR_DIR = ENV_DOT_VENV_DIR / 'var'

BSSENV_VERSION_FILE = ENV_CONFIG_DIR / 'bssenv_version'
BSSENV_INSTALL_TYPE_FILE = ENV_CONFIG_DIR / 'install_type'

# ENVIRONMENTS
BSSENV_ENVIRONMENTS_FILE = Path(
    (ENV_CONFIG_DIR / 'bssenv_environments').read_text().strip())
BSSENV_ENVIRONMENTS_LOCK_FILE = f'{BSSENV_ENVIRONMENTS_FILE}.lock'

# DOCKER
ENV_DOCKER_VOLUMES_DIR = ENV_DOCKER_DIR / 'volumes'
ENV_DOCKER_DATA_VOLUME = ENV_DOCKER_VOLUMES_DIR / 'bss_data'
ENV_DOCKER_CONFIG_VOLUME = ENV_DOCKER_VOLUMES_DIR / 'bss_config'
ENV_DOCKER_LOGS_VOLUME = ENV_DOCKER_VOLUMES_DIR / 'bss_logs'

# COMPOSEFILES
ENV_COMPOSEFILES_DIR = ENV_DOCKER_DIR / 'composefiles'
ENV_MAIN_COMPOSEFILE_FILE = ENV_COMPOSEFILES_DIR / 'daemons.yml'
ENV_COMPOSEFILES_COMMANDS_DIR = ENV_COMPOSEFILES_DIR / 'commands'
ENV_COMPOSEFILES_DATA_PROVIDERS_DIR = ENV_COMPOSEFILES_DIR / 'data_providers'

# TEMPLATES
ENV_TEMPLATE_COMPOSEFILE_FILE = ENV_TEMPLATES_DIR / 'composefiles/template.yml'
ENV_TEMPLATE_SHELL_COMMAND_FILE = ENV_TEMPLATES_DIR / 'shell/command.py'
ENV_TEMPLATE_SHELL_SERVICE_COMMAND_FILE = \
    ENV_TEMPLATES_DIR / 'shell/serviceCommand.py'
ENV_PORT_TEMPLATES_DIR = ENV_TEMPLATES_DIR / 'ports'

ENV_INSTALLED_CONFIG_MAPS_FILE = ENV_VAR_DIR / 'installed_config_maps'
ENV_UNINSTALLED_CONFIG_MAPS_FILE = ENV_VAR_DIR / 'uninstalled_config_maps'
ENV_INSTALLED_SERVICES_FILE = ENV_VAR_DIR / 'installed'
ENV_UNINSTALLED_SERVICES_FILE = ENV_VAR_DIR / 'uninstalled'
ENV_INITIALIZED_SERVICES_FILE = ENV_VAR_DIR / 'initialized'
ENV_ADDED_DNS_MAPPINGS_FILE = ENV_VAR_DIR / 'dns_mappings'
ENV_CHANGED_PORT_MAPPINGS_FILE = ENV_VAR_DIR / 'port_mappings'
ENV_SWITCHES_FILE = ENV_VAR_DIR / 'switches'
ENV_LOCKS_DIR = ENV_VAR_DIR / 'locks'

# COMMAND REGISTRY
ENV_COMMAND_REGISTRY_DIR = ENV_VAR_DIR / 'command_registry'
ENV_COMMAND_REGISTRY_FILE = ENV_COMMAND_REGISTRY_DIR / 'registry.yml'
