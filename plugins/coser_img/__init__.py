from nonebot import on_command
from nonebot.adapters.cqhttp import MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests

coser = on_command('cos', aliases={'coser', 'COS', 'Cos', 'cOS', 'coS'}, priority=5, block=True)

_coser_url = 'http://api.rosysun.cn/cos'


@coser.handle()
async def _(bot: Bot, event: Event, state: T_State):
    img_url = requests.get(_coser_url).text
    await coser.send(MessageSegment.image(img_url))
