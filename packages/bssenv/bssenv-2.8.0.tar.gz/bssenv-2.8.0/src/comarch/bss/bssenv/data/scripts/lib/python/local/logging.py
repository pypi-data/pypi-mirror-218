import sys
import os
import logging
import logging.handlers
from pathlib import Path
from functools import partial
from local.paths import ENV_MAIN_LOG_FILE
import comarch.bss.bssenv as BSSENV_PKG

# add custom paths to python site packages
SCRIPT_DIR = Path(__file__).resolve().parent
LIBS_DIR = SCRIPT_DIR.parent
BSSENV_PYT_SITE_PKGS = Path(BSSENV_PKG.__file__).resolve().parent / \
    'data' / 'python_site_packages'
sys.path = [str(BSSENV_PYT_SITE_PKGS), str(LIBS_DIR)] + sys.path

# import from custom site packages

# log levels
CRITICAL = logging.CRITICAL  # console + file                               :50
ERROR = logging.ERROR  # console + file                                     :40
WARNING = logging.WARNING  # console + file                                 :30
SPEAK = 25  # console + file                                                :25
INFO = logging.INFO  # file, default, for ordinary users                    :20
DEBUG = logging.DEBUG  # file, debug messages, not for ordinary users       :10
NOTSET = logging.NOTSET  # not set                                          :00

# additional log level
logging.addLevelName(SPEAK, "SPEAK")

# main logger
logger = logging.getLogger()
logger.setLevel(getattr(logging, os.environ.get(
    'BSSENV_LOG_LEVEL', 'INFO').upper()))

# file handler
if ENV_MAIN_LOG_FILE.parent.exists():
    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s '
        '[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s')
    file_handler = logging.handlers.TimedRotatingFileHandler(
        str(ENV_MAIN_LOG_FILE),
        when="midnight",
        interval=1,
        backupCount=14)
    file_handler.setLevel(logging.DEBUG)  # log all messages to file
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


class StdoutFilter(logging.Filter):

    def filter(self, rec):
        # only records that are not critical, errors or warnings
        return rec.levelno < WARNING


# console stdout handler
console_formatter = logging.Formatter('%(message)s')  # just plain text
console_handler = logging.StreamHandler(sys.stdout)  # this goes to stdout
if os.environ.get('BSSENV_VERBOSE_MODE', 'false').lower() == 'false':
    console_handler.setLevel(SPEAK)  # log only important messages to console
else:
    console_handler.setLevel(INFO)  # log a little bit more messages to console. But still less then to file  # noqa: E501
console_handler.setFormatter(console_formatter)
console_handler.addFilter(StdoutFilter())
logger.addHandler(console_handler)

# console stderr handler
console_handler = logging.StreamHandler()  # this goes to stderr
console_handler.setLevel(WARNING)  # log only important messages to console
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# export logging functions
critical = logger.critical
error = logger.error
warning = logger.warning
speak = partial(logger.log, SPEAK)
info = logger.info
debug = logger.debug
log = logger.log


# for debug purposes
def list_loggers():
    rootlogger = logging.getLogger()
    print(rootlogger)
    for h in rootlogger.handlers:
        print('     %s' % h)
    for nm, lgr in logging.Logger.manager.loggerDict.items():
        print('+ [%-20s] %s ' % (nm, lgr))
        if not isinstance(lgr, logging.PlaceHolder):
            for h in lgr.handlers:
                print('     %s' % h)
