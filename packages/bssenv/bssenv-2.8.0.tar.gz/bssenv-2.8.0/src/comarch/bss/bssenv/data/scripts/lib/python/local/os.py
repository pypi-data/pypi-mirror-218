import sys
import os
import shutil
import subprocess
import socket
import threading
import locale
from os import PathLike
from pathlib import Path
from subprocess import PIPE, STDOUT
from typing import Union, List, Tuple
from functools import partial, lru_cache
from local.regex import is_like
from local.cache import FileCacheEntry, Cache
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR = Path(__file__).resolve().parent
LIBS_DIR = SCRIPT_DIR.parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / 'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS), str(LIBS_DIR)] + sys.path

# import from custom site packages


lock = threading.RLock()
Cache = Cache()


# run, do not catch output, check exit code
run = partial(subprocess.run, check=True)


# run, do not catch output, do not check exit code
run2 = partial(subprocess.run, check=False)


# run, catch output, check exit code
exec = partial(subprocess.run, stdout=PIPE, stderr=PIPE, encoding=locale.getpreferredencoding(), check=True)


# run, catch output, do not check exit code
exec2 = partial(subprocess.run, stdout=PIPE, stderr=PIPE, encoding=locale.getpreferredencoding(), check=False)


# run, save output to given file, check exit code
class fexec:

    __cmd: Union[str, List, Path] = None
    __args = []
    __kwargs = dict()

    def __call__(
            self,
            cmd: Union[str, List, Path],
            *args,
            **kwargs) -> 'fexec':
        instance = self.__class__()
        instance.__cmd = cmd
        instance.__args = args
        instance.__kwargs = kwargs
        return instance

    def __rshift__(self, path: Union[str, Path]) -> subprocess.CompletedProcess:
        # append to file: >> path_like
        if self.__cmd is not None:
            path = Path(path)
            stderr = STDOUT
            with open(path, 'a') as stdout:
                return run(self.__cmd, *self.__args, stdout=stdout, stderr=stderr, **self.__kwargs)

    def __gt__(self, path: Union[str, Path]) -> subprocess.CompletedProcess:
        # overwrite file: > path_like
        if self.__cmd is not None:
            path = Path(path)
            stderr = STDOUT
            with open(path, 'w') as stdout:
                return run(self.__cmd, *self.__args, stdout=stdout, stderr=stderr, **self.__kwargs)


# # run, save output to given file, do not check exit code
class fexec2:

    __cmd: Union[str, List, Path] = None
    __args = []
    __kwargs = dict()

    def __call__(
            self,
            cmd: Union[str, List, Path],
            *args,
            **kwargs) -> 'fexec':
        instance = self.__class__()
        instance.__cmd = cmd
        instance.__args = args
        instance.__kwargs = kwargs
        return instance

    def __rshift__(self, path: Union[str, Path]) -> subprocess.CompletedProcess:
        # append to file: >> path_like
        if self.__cmd is not None:
            path = Path(path)
            stderr = STDOUT
            with open(path, 'a') as stdout:
                return run2(self.__cmd, *self.__args, stdout=stdout, stderr=stderr, **self.__kwargs)

    def __gt__(self, path: Union[str, Path]) -> subprocess.CompletedProcess:
        # overwrite file: > path_like
        if self.__cmd is not None:
            path = Path(path)
            stderr = STDOUT
            with open(path, 'w') as stdout:
                return run2(self.__cmd, *self.__args, stdout=stdout, stderr=stderr, **self.__kwargs)


fexec = fexec()  # singleton
fexec2 = fexec2()  # singleton


@lru_cache(maxsize=1)
def ip_address():
    ip_address = os.environ.get('BSSENV_IP', None)
    if ip_address is None or not is_like(ip_address, '^[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+$'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip_address = s.getsockname()[0]
        except Exception:
            ip_address = '127.0.0.1'
        finally:
            s.close()
    return ip_address


@lru_cache(maxsize=1)
def hostname() -> str:
    return os.environ.get('BSSENV_HOSTNAME', None) or exec(['hostname', '-f']).stdout.strip()


def get_system_cpu_cores_number():
    return os.cpu_count()


def is_dir_empty(path):
    with os.scandir(str(path)) as it:
        if any(it):
            return False
    return True


def create_dir(path):
    os.makedirs(str(path), exist_ok=True)


def create_relative_symbolic_link(src, dst):
    src = Path(src)
    dst = Path(dst)
    os.symlink(str(os.path.relpath(src, dst.parent)), str(dst))


def get_uid_gid(path: PathLike = None) -> Tuple[int, int]:
    if path is None:
        return os.geteuid(), os.getegid()
    else:
        statinfo = os.stat(str(path))
        return statinfo.st_uid, statinfo.st_gid


def chown(path, uid, gid):
    path = Path(path)
    os.chown(str(path), uid, gid)
    if path.is_dir():
        for root, dirs, files in os.walk(str(path)):
            for _ in dirs:
                os.chown(os.path.join(root, _), uid, gid)
            for _ in files:
                os.chown(os.path.join(root, _), uid, gid)


def remove_path(path):
    path = Path(path)
    if path.exists():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(str(path))


def copy_path(src, dst):
    src = Path(src)
    dst = Path(dst)
    if src.is_file():
        shutil.copyfile(str(src), str(dst))
    elif src.is_dir():
        shutil.copytree(str(src), str(dst))


# very simple file caching. Be careful: do not load huge files
def get_cached_file(path: Union[str, Path]):
    with lock:
        path = Path(path).resolve()
        if not Cache.exists(path):
            Cache.add(FileCacheEntry(path))
        return Cache.get(path)


def use_raw_output() -> bool:
    return os.getenv('BSSENV_STDOUT_TYPE', None) in ('json', 'yaml', 'yml')
