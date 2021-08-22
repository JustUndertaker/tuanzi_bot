from nonebot.log import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from pydantic import Field, BaseSettings


class Config(BaseSettings):
    apscheduler_autostart: bool = True
    apscheduler_log_level: int = 30
    apscheduler_config: dict = Field(
        default_factory=lambda: {"apscheduler.timezone": "Asia/Shanghai"})

    class Config:
        extra = "ignore"


plugin_config = Config()
APSscheduler = AsyncIOScheduler()


async def start_scheduler():
    if not APSscheduler.running:
        APSscheduler.configure(plugin_config.apscheduler_config)
        APSscheduler.start()
        logger.opt(colors=True).info("<y>Scheduler Started</y>")
