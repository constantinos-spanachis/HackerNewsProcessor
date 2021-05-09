import logging
import sys


class Logger(object):
    _format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    _dt_fmt = '%Y-%m-%d %H:%M'
    _console_handler = logging.StreamHandler(sys.stdout)
    _formatter = logging.Formatter(fmt=_format, datefmt=_dt_fmt)
    _console_handler.setFormatter(_formatter)
    _console_handler.setLevel(logging.DEBUG)
    _warning_file_handler = logging.FileHandler(filename="logger_warnings.txt")
    _warning_file_handler.setFormatter(_formatter)
    _warning_file_handler.setLevel(logging.WARNING)
    _error_file_handler = logging.FileHandler(filename="logger_errors.txt")
    _error_file_handler.setFormatter(_formatter)
    _error_file_handler.setLevel(logging.ERROR)
    logger = None

    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self._console_handler)
        self.logger.addHandler(self._error_file_handler)
        self.logger.addHandler(self._warning_file_handler)
