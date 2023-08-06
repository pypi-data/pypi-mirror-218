import logging
import os
import tempfile
from datetime import datetime
from dateutil import parser
from io import BytesIO
from typing import Final, TextIO
from pypomes_core import APP_PREFIX, DATETIME_FORMAT_INV, env_get_str

LOGGING_ID: Final[str] = env_get_str(f"{APP_PREFIX}_LOGGING_ID", f"{APP_PREFIX}")
LOGGING_FORMAT: Final[str] = env_get_str(f"{APP_PREFIX}_LOGGING_ID",
                                         "{asctime} {levelname:1.1} {thread:5d} "
                                         "{module:20.20} {funcName:20.20} {lineno:3d} {message}")
LOGGING_STYLE: Final[str] = env_get_str(f"{APP_PREFIX}_LOGGING_STYLE", "{")

LOGGING_FILE_PATH: Final[str] = env_get_str(f"{APP_PREFIX}_LOGGING_FILE_PATH",
                                            os.path.join(tempfile.gettempdir(), f"{APP_PREFIX}.log"))
LOGGING_FILE_MODE: Final[str] = env_get_str(f"{APP_PREFIX}_LOGGING_FILE_MODE", "a")

# define and configure the logger
PYPOMES_LOGGER: Final[logging.Logger] = logging.getLogger(LOGGING_ID)

match env_get_str(f"{APP_PREFIX}_LOGGING_LEVEL"):
    case "d" | "debug":
        LOGGING_LEVEL: Final[int] = logging.DEBUG
    case "i" | "info":
        LOGGING_LEVEL: Final[int] = logging.INFO
    case "w" | "warning":
        LOGGING_LEVEL: Final[int] = logging.WARN
    case "e" | "error":
        LOGGING_LEVEL: Final[int] = logging.ERROR
    case "c" | "critical":
        LOGGING_LEVEL: Final[int] = logging.CRITICAL
    case _:
        LOGGING_LEVEL: Final[int] = logging.NOTSET

logging.basicConfig(level=LOGGING_LEVEL,
                    filename=LOGGING_FILE_PATH,
                    filemode=LOGGING_FILE_MODE,
                    datefmt=DATETIME_FORMAT_INV,
                    style="{",
                    format="{asctime} {levelname:1.1} {thread:5d} "
                           "{module:20.20} {funcName:20.20} {lineno:3d} {message}")
for _handler in logging.root.handlers:
    _handler.addFilter(logging.Filter(LOGGING_ID))


def logging_get_entries(errors: list[str], log_level: str, log_from: str, log_to: str) -> BytesIO:

    def get_level(level: str) -> int:

        result: int | None
        match level:
            case "d" | "debug":
                result = logging.DEBUG          # 10
            case "i" | "info":
                result = logging.INFO           # 20
            case "w" | "warning":
                result = logging.WARN           # 30
            case "e" | "error":
                result = logging.ERROR          # 40
            case "c" | "critical":
                result = logging.CRITICAL       # 50
            case _:
                result = logging.NOTSET         # 0

        return result

    # inicializa variável de retorno
    result: BytesIO | None = None

    # obtain the logging level
    logging_level: int = get_level(log_level)

    # obtain the initial timestap
    from_stamp: datetime | None = None
    if log_from is not None:
        from_stamp = parser.parse(log_from)
        if from_stamp is None:
            errors.append(f"Value '{from_stamp}' of 'from' attribute invalid")

    # obtaind the final timestamp
    to_stamp: datetime | None = None
    if log_to is not None:
        to_stamp = parser.parse(log_to)
        if to_stamp is None or \
           (from_stamp is not None and from_stamp > to_stamp):
            errors.append(f"Value '{to_stamp}' of 'to' attribute invalid")

    # does the log file exist ?
    if not os.path.exists(LOGGING_FILE_PATH):
        # no, report the error
        errors.append(f"File '{LOGGING_FILE_PATH}' not found")

    # any error ?
    if len(errors) == 0:
        # no, proceed
        result = BytesIO()
        with open(LOGGING_FILE_PATH, "r") as f:
            line: str = f.readline()
            while line:
                items: list[str] = line.split(maxsplit=3)
                level: int = get_level(items[2])
                if level >= logging_level:
                    timestamp: datetime = parser.parse(f"{items[0]} {items[1]}")
                    if (from_stamp is None or timestamp >= from_stamp) and \
                       (to_stamp is None or timestamp <= to_stamp):
                        result.write(line.encode())
                line = f.readline()

    return result


def logging_log_msgs(msgs: list[str], log_level: str = None, output_dev: TextIO = None):
    """
    Write messages in *msgs* to *PYPOMES_LOGGER*, and to *output_dev*
    (tipically, *sys.stdout* ou *sys.stderr*).

    :param msgs: the messages list
    :param log_level: the logging level (None for no log printing)
    :param output_dev: output device where the message is to be printed (None for no device printing)
    """
    # traverse the messages list
    for msg in msgs:
        # write the message
        match log_level:
            case "c" | "critical":
                PYPOMES_LOGGER.critical(msg)
            case "d" | "debug":
                PYPOMES_LOGGER.debug(msg)
            case "i" | "info":
                PYPOMES_LOGGER.info(msg)
            case "w" | "warning":
                PYPOMES_LOGGER.warning(msg)
            case "e" | "error":
                PYPOMES_LOGGER.error(msg)

        # o dispositivo de saída foi definido ?
        if output_dev is not None:
            # sim, escreva o erro nesse dispositivo
            output_dev.write(msg)

            # o dispositivo de saída é 'stderr' ou 'stdout' ?
            if output_dev.name.startswith("<std"):
                # sim, mude de linha
                output_dev.write("\n")
