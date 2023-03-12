from pathlib import Path
from padme_conductor._TrainTagFormatter import _TrainTagFormatter
from typing import List, Union
import logging
import sys
import padme_conductor.constants as constants


class TrainLogger:
    _LOGGING_DIR = "logs"
    OptionalHandlers = Union[List[Union[logging.FileHandler, logging.StreamHandler]], None]

    def __init__(self, handlers: OptionalHandlers = None) -> None:
        self.log_path = Path(constants._WORK_DIR_NAME) / TrainLogger._LOGGING_DIR
        self.log_file = self.log_path / "logfile.log"

        self.log_path.mkdir(parents=True, exist_ok=True)
        self.pc_logger = logging.getLogger(__name__)
        self.pc_logger.setLevel(logging.DEBUG)
        self.log_formatter = _TrainTagFormatter(datefmt="%Y-%m-%d %H:%M:%S")
        self._handlers = handlers

    def log(self, log_level: int, msg: object, *args: object, extra=None):
        if self._handlers is None:
            self.register_default_handlers()
        self.pc_logger.log(log_level, msg, *args, extra=extra)

    def _run_once(f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)

        wrapper.has_run = False
        return wrapper

    @_run_once
    def register_default_handlers(self):
        self.file_handler = logging.FileHandler(filename=self.log_file)
        self.file_handler.setLevel(logging.INFO)

        self.stdout_handler = logging.StreamHandler(stream=sys.stdout)
        self.stdout_handler.setLevel(logging.DEBUG)
        self.stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)

        self.stderr_handler = logging.StreamHandler(stream=sys.stderr)
        self.stderr_handler.setLevel(logging.ERROR)

        self._handlers = [
            self.file_handler,
            self.stdout_handler,
            self.stderr_handler,
        ]

        for handler in self._handlers:
            handler.setFormatter(self.log_formatter)
            self.pc_logger.addHandler(handler)

    def log_ml(self):
        raise NotImplementedError