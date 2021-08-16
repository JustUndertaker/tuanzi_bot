import loguru
from configs.pathConfig import LOG_PATH

logger = loguru.logger

custom_format = "{time:MM-DD HH:MM:SS} [{name}] [{level}] | {message}"

logger.add(
    LOG_PATH+"debug/{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="10 days",
    level="DEBUG",
    format=custom_format,
    encoding="utf-8"
)

logger.add(
    LOG_PATH+"info/{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="10 days",
    level="INFO",
    format=custom_format,
    encoding="utf-8"
)

logger.add(
    LOG_PATH+"error/{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="10 days",
    level="ERROR",
    format=custom_format,
    encoding="utf-8"
)
