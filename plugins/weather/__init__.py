from nonebot.adapters.cqhttp import Bot, Event
from nonebot import on_command
from nonebot.typing import T_State
from .data_source import get_weather_of_city


__plugin_name__ = '天气查询'
__plugin_usage__ = "普普通通的查天气吧\n示例：北京天气"

weather = on_command("天气", priority=5, block=True)


@weather.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    city = args
    msg = await get_weather_of_city(city)
    await weather.finish(msg)
