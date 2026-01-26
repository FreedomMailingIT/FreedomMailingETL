"""
Setting up logger as class.  Using 'filename' rather than 'module' to get
the actual program/lineno that was logger called from.

Explanation:
- get a logger (with name if needed)
- set the level of the log

- define the log handler
- define the format of log entries
- set the format to the handler
- add the handler to the log
"""


import logging
import inspect
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app_modules import file_locations


FILE_PATH = file_locations.FILE_PATH
LOG_FILE = file_locations.LOG_FILE


def singleton(cls):
    """Make decorated class a singleton."""
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class AppLogger:
    """
    Logger using 'filename' (not 'module') to record program logger called from.
    """
    class CustomFormatter(logging.Formatter):
        """Custom formatter that injects custom attributes into log records."""
        def format(self, record):
            for caller in inspect.stack():
                if 'utils.logger' in caller.code_context[0]:  # find appropriate stack item
                    record.caller_name = Path(caller.filename).stem
                    record.caller_lineno = caller.lineno
                    break
            return super().format(record)

    def __init__(self):
        self.logger = logging.getLogger('')
        self.logger.setLevel(logging.DEBUG if '/tests/' in FILE_PATH else logging.INFO)

        # Create a file handler
        file_handler = RotatingFileHandler(
            f'{FILE_PATH}{LOG_FILE}',
            maxBytes=1e6, backupCount=3, encoding='utf8'
            )
        fmt = "[%(levelname).1s %(asctime)s %(caller_name)s:%(caller_lineno)d] %(message)s"
        file_handler.setFormatter(self.CustomFormatter(fmt=fmt, datefmt="%y%m%d %H:%M:%S"))
        self.logger.addHandler(file_handler)

        if 'projects' in FILE_PATH:  # only add console if development system
            console_handler = logging.StreamHandler()
            fmt = "[%(levelname).1s %(caller_name)s:%(caller_lineno)d] %(message)s"
            console_handler.setFormatter(self.CustomFormatter(fmt=fmt))
            self.logger.addHandler(console_handler)

    def log(self, level, message):
        """Logs a message with the custom username attribute."""
        self.logger.log(level, message)

    def debug(self, message, *args, exc_info=False):
        """Handle DEBUG call."""
        self.logger.debug(message, *args, exc_info=exc_info)

    def info(self, message, *args, exc_info=False):
        """Handle INFO call."""
        self.logger.info(message, *args, exc_info=exc_info)

    def warning(self, message, *args, exc_info=False):
        """Handle WARNING call."""
        self.logger.warning(message, *args, exc_info=exc_info)

    def error(self, message, *args, exc_info=False):
        """Handle ERROR call."""
        self.logger.error(message, *args, exc_info=exc_info)

    def critical(self, message, *args, exc_info=False):
        """Handle CRITICAL call."""
        self.logger.critical(message, *args, exc_info=exc_info)


logger = AppLogger()
