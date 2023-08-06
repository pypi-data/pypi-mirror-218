# imports from normal python site packages
import sys
import abc
import os
from typing import Any, Dict, List, Callable, Union
from pathlib import Path
from copy import deepcopy
from local.logging import debug
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR_PATH = Path(__file__).resolve().parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / 'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS)] + sys.path

# import from custom site packages
import blessed
from rich.console import Console
from rich.table import Table
from rich import box, print as rprint
from deepdiff import DeepDiff
import local.yaml as yaml
import json
from local.os import use_raw_output


term = blessed.Terminal()
console = Console()


class DataUpdater:

    @abc.abstractmethod
    def update(data: Any) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get() -> Any:
        raise NotImplementedError


class DataPrinter:

    @abc.abstractmethod
    def print(self, data: Any) -> None:
        raise NotImplementedError


Header = val = str
Headers = List[Header]
Row = Dict[Header, val]


class DictTabularDataPrinter(DataPrinter):

    def print(self, data: Dict[str, Dict[str, str]]) -> None:
        raw_type = os.getenv('BSSENV_STDOUT_TYPE', None)
        if raw_type == 'json':
            raw_data = {_: __['_ROWS_'] for _, __ in data.items()}
            print(json.dumps(raw_data))
        elif raw_type in ('yaml', 'yml'):
            raw_data = {_: __['_ROWS_'] for _, __ in data.items()}
            print(yaml.dict_to_str(raw_data))
        else:
            for table_name, table in data.items():
                show_header = False
                headers = []
                if '_METADATA_' in table.keys():
                    title = table['_METADATA_'].get('title', None)
                    if title:
                        rprint(f'[italic]{title}')
                    show_header = table['_METADATA_'].get('show_header', False)
                    headers = table['_METADATA_'].get('headers', [])
                table_to_print = Table(show_header=show_header, box=box.SIMPLE)
                for header in headers:
                    if type(header) == dict:
                        kwargs = {_: __ for _, __ in header.items() if _ != 'name'}
                        header = header['name']
                        table_to_print.add_column(header, **kwargs)
                    elif type(header) == str:
                        table_to_print.add_column(header)
                for row in table['_ROWS_']:
                    row_cells = \
                        ((row[_['name']] if type(_) == dict else row[_]) for _ in headers) \
                        if header else row.values()
                    table_to_print.add_row(*row_cells)
                console.print(table_to_print)


class DictDataUpdater(DataUpdater):

    @property
    def data(self) -> Dict:
        return getattr(self, '_DictDataUpdater__data', None)

    @data.setter
    def data(self, data: Dict) -> None:
        self.__data = data

    def update(self, data: Dict) -> bool:
        debug(f'update: {data}')
        previous_data = self.data
        self.data = deepcopy(data)
        if data is None:
            raise Exception("Data parameter can't be None")
        if previous_data is None:
            return True
        return True \
            if len(DeepDiff(data, previous_data, ignore_order=True, report_repetition=True).keys()) > 0 else False

    def get(self) -> Dict:
        return self.data


class Screen:

    def __init__(
            self, terminal: blessed.Terminal, data_updater: DataUpdater, data_printer: DataPrinter,
            data_transformer: Callable[[Any], Any] = None, use_secondary_screen_buffer: bool = True) -> None:
        self.__terminal = terminal
        self.__data_updater = data_updater
        self.__data_printer = data_printer
        self.__data_transofmer = data_transformer
        self.__term_height = None
        self.__term_width = None
        self.__use_secondary_screen_buffer = use_secondary_screen_buffer

    @property
    def term(self) -> blessed.Terminal:
        return self.__terminal

    def destroy(self):
        if getattr(self, '_Screen__hidden_cursor', None) is not None:
            self.__hidden_cursor.__exit__(None, None, None)
            self.__cbreak.__exit__(None, None, None)
            self.__screen.__exit__(None, None, None)
            del self.__hidden_cursor
            del self.__cbreak
            del self.__screen

    def __init_secondary_screen(self):
        screen_updated = False
        if getattr(self, '_Screen__screen', None) is None:
            # create screen
            self.__screen = self.term.fullscreen()
            self.__screen.__enter__()
            self.__hidden_cursor = self.term.hidden_cursor()
            self.__hidden_cursor.__enter__()
            self.__cbreak = self.term.cbreak()
            self.__cbreak.__enter__()
            self.__term_height = self.term.height
            self.__term_width = self.term.width
            screen_updated = True
        if self.__term_height is not None and self.__term_width is not None:
            term_height = self.__term_height
            term_width = self.__term_width
            self.__term_height = self.term.height
            self.__term_width = self.term.width
            debug(f'__height: {self.__term_height}')
            debug(f'__width: {self.__term_width}')
            debug(f'term.height: {self.term.height}')
            debug(f'term.width: {self.term.width}')
            if term_height != self.__term_height or term_width != self.__term_width:
                # terminal has changed it's dimensions
                debug(f'Terminal dimensions change detected')
                screen_updated = True
                self.__reset_position()
                self.__clear_screen()
                self.__data_printer.print(self.__data_updater.get())
        return screen_updated

    def __reset_position(self) -> None:
        print(self.term.home + self.term.normal)

    def __clear_screen(self) -> None:
        print(self.term.clear)

    def update(self, data: Any, reset_position: bool = True, clear_screen: bool = True) -> Union[bool, None]:
        screen_updated = False
        if use_raw_output() is False and self.__use_secondary_screen_buffer:
            debug(f'use_raw_output(): {use_raw_output()}')
            screen_updated = self.__init_secondary_screen()
        data = self.__data_transofmer(data) if self.__data_transofmer is not None else data
        if self.__data_updater.update(data):
            debug(f'screen.update.true: {data}')
            screen_updated = True
            if use_raw_output() is False:
                if reset_position:
                    self.__reset_position()
                if clear_screen:
                    self.__clear_screen()
            self.__data_printer.print(self.__data_updater.get())
        return screen_updated


class InteractiveScreen(Screen):

    def update(self, data: Any) -> Union[bool, None]:
        updated = super().update(data)
        if updated:
            print(f"{self.term.black_on_skyblue}press 'q' to quit.{self.term.normal}\n")
        if self.term.inkey(timeout=2) == 'q':
            self.destroy()
            return None
        return updated
