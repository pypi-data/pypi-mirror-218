import sys
import os
import abc
from local.logging import debug
from pathlib import Path
from typing import Union, Dict, Any
import local.yaml
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages


Cache_key = Any


class CacheReloader:

    @abc.abstractmethod
    def is_invalidated(self) -> bool:
        # is source invalidated
        raise NotImplementedError()

    @abc.abstractmethod
    def reload(self) -> Any:
        # reload source into self.value and return it
        raise NotImplementedError()


class CacheTransformer:

    @abc.abstractmethod
    def transform(self) -> Any:
        # transform self.value into transformed(self.value) and return it
        raise NotImplementedError()


class CacheEntry(CacheReloader, CacheTransformer):

    def __init__(self, key: Cache_key):
        self.__key = key
        self.__value = None

    @property
    def key(self) -> Cache_key:
        return self.__key

    @property
    def value(self) -> Any:
        return self.__value

    @value.setter
    def value(self, value) -> None:
        self.__value = value


class FakeCacheReloader(CacheReloader):

    def is_invalidated(self) -> bool:
        # never invalidated
        return False

    def reload(self) -> Any:
        # never reload
        return self.value


class FakeCacheTransformer(CacheTransformer):

    def transform(self) -> Any:
        # do not transform at all
        return self.value


class ConstantCacheEntry(CacheEntry, FakeCacheReloader, FakeCacheTransformer):

    def __init__(self, key: Cache_key):
        self.__key = key
        self.__value = key


class FileCacheReloader(CacheReloader):

    def __init__(self, path: Union[str, Path]):
        self.__path = Path(path)
        self.__mtime = None

    def is_invalidated(self) -> bool:
        if self.__mtime is None:
            # not loaded to cache yet
            return True
        else:
            if not self.__path.exists():
                # file was deleted
                return True
            else:
                # check if file has changed
                mtime = os.path.getmtime(self.__path)
                if self.__mtime != mtime:
                    return True
        return False

    def reload(self) -> Union[str, None]:
        if not self.__path.exists():
            self.value = None
            self.__mtime = None
        else:
            self.__mtime = os.path.getmtime(self.__path)
            self.value = self.__path.read_text()
        debug(f'FileCacheReloader.reload: {self.__path}')
        # debug(f'FileCacheReloader.reload: {self.__path}\n{self.value}')
        return self.value


class FileCacheEntry(CacheEntry, FileCacheReloader, FakeCacheTransformer):

    def __init__(self, path: Union[str, Path]):
        path = Path(path)
        CacheEntry.__init__(self, key=path)
        FileCacheReloader.__init__(self, path=path)


class YamlCacheTransformer(CacheTransformer):

    def transform(self) -> Dict:
        if self.value is not None:
            self.value = local.yaml.str_to_dict(self.value)
        return self.value


class YamlFileCacheEntry(YamlCacheTransformer, FileCacheEntry):
    pass


class Cache:

    def __init__(self):
        self.__cache: Dict[Cache_key, CacheEntry] = dict()

    def exists(self, cache_key: Cache_key) -> bool:
        return cache_key in self.__cache.keys()

    def add(self, cache_entry: CacheEntry) -> None:
        if not self.exists(cache_entry.key):
            self.__cache[cache_entry.key] = cache_entry

    def delete(self, cache_key: Cache_key) -> None:
        if self.exists(cache_key):
            del self.__cache[cache_key]

    def get_entry(self, cache_key: Cache_key) -> CacheEntry:
        if not self.exists(cache_key):
            raise Exception(f'Cache key "{cache_key}" not found')
        return self.__cache[cache_key]

    def get(self, cache_key: Cache_key) -> Any:
        cache_entry = self.get_entry(cache_key)
        if cache_entry.is_invalidated():
            cache_entry.reload()
            cache_entry.transform()
        return cache_entry.value


class SharedMultiFileCacheReloader(CacheReloader):

    def __init__(self, cache: Cache):
        self.__cache = Cache()

    def is_invalidated(self, path: Union[str, Path]) -> bool:
        path = Path(path)
        if not self.__cache.exists(path):
            return True
        else:
            return self.__cache.get_entry(path).is_invalidated()

    def reload(self, path: Union[str, Path]) -> Union[None, str]:
        path = Path(path)
        if not self.__cache.exists(path):
            self.__cache.add(FileCacheEntry(path))
        self.value = self.__cache.get(path)
        debug(f'FileCacheReloader.reload: {path}')
        # debug(f'FileCacheReloader.reload: {path}\n{self.value}')
        return self.value
