import sys as _sys
import atexit as _atexit
from loguru import _defaults
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger
from configs.pathConfig import LOG_PATH
from nonebot.log import default_filter, default_format

logger = _Logger(_Core(), None, 0, False, False, False, False, True, None, {})

_atexit.register(logger.remove)

custom_format = "{time:MM-DD HH:MM:SS} [{name}] [{level}] | {message}"

if _defaults.LOGURU_AUTOINIT and _sys.stderr:
    logger.add(_sys.stderr,
               filter=default_filter,
               format=default_format,
               level='INFO')

logger.add(
    LOG_PATH+"debug/{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="10 days",
    level="DEBUG",
    format=custom_format,
    filter=default_filter,
    encoding="utf-8"
)

logger.add(
    LOG_PATH+"info/{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="10 days",
    level="INFO",
    format=custom_format,
    filter=default_filter,
    encoding="utf-8"
)

logger.add(
    LOG_PATH+"error/{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="10 days",
    level="ERROR",
    format=custom_format,
    filter=default_filter,
    encoding="utf-8"
)
