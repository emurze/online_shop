import logging
from enum import Enum

LOG_FORMAT_DEBUG = (
    "%(levelname)s:     %(message)s  %(pathname)s:%(funcName)s:%(lineno)d"
)
DEFAULT_LOG_FORMAT = "%(levelname)s:     %(message)s"


class LogLevel(str, Enum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging(log_level: str | None, debug: bool) -> None:
    if not log_level:
        log_level = LogLevel.debug if debug else LogLevel.warning

    log_level = log_level.upper()

    if log_level not in list(LogLevel):
        # We use LogLevel.error as the default log level
        logging.basicConfig(level=LogLevel.error)

    elif log_level == LogLevel.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)

    else:
        logging.basicConfig(level=log_level, format=DEFAULT_LOG_FORMAT)
