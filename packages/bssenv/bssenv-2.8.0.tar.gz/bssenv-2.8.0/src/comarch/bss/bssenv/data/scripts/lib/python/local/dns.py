# imports from normal python site packages
import sys
import threading
from pathlib import Path
from typing import Set
from local.cache import FileCacheEntry, Cache
import local.paths
import local.os
import local.install
import local.services
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


lock = threading.RLock()
Cache = Cache()
ENV_ADDED_DNS_MAPPINGS_FILE = local.paths.ENV_ADDED_DNS_MAPPINGS_FILE


def get_added_dns_mappings() -> Set[str]:
    with lock:
        if not Cache.exists(ENV_ADDED_DNS_MAPPINGS_FILE):
            Cache.add(FileCacheEntry(ENV_ADDED_DNS_MAPPINGS_FILE))
        return set(Cache.get(ENV_ADDED_DNS_MAPPINGS_FILE).splitlines())


def set_added_dns_mappings(*dns_mappings: str) -> None:
    with lock:
        ENV_ADDED_DNS_MAPPINGS_FILE.write_text("\n".join(set(dns_mappings)))


def add_dns_mappings(*dns_mappings: str) -> None:
    if len(dns_mappings) > 0:
        all_dns_mappings = get_added_dns_mappings()
        all_dns_mappings |= set(dns_mappings)
        set_added_dns_mappings(*all_dns_mappings)


def remove_dns_mappings(*dns_names: str) -> None:
    if len(dns_names) > 0:
        dns_names = set(dns_names)
        all_dns_mappings = list(
            _ for _ in get_added_dns_mappings()
            if _.split(':')[0] not in dns_names)
        set_added_dns_mappings(*all_dns_mappings)
    else:
        with lock:
            ENV_ADDED_DNS_MAPPINGS_FILE.write_text('')
