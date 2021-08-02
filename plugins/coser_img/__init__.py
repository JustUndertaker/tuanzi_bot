import httpx
from nonebot import on_command
from nonebot.log import logger
from nonebot.adapters.cqhttp import MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

coser = on_command('cos', aliases={'coser', 'COS', 'Cos', 'cOS', 'coS'}, priority=5, block=True)

_rosysun_url = 'http://api.rosysun.cn/cos'


@coser.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # 只匹配cos纯指令，后续带任何字符都不作处理
    msg = event.get_plaintext()
    if len(msg) == 0:
        message = _img_from_rosysun()
        await coser.finish(message)


def _img_from_rosysun() -> MessageSegment:
    r = httpx.get(_rosysun_url)
    code = r.status_code
    if code == 200:
        img_url = r.text
        message = MessageSegment.image(img_url)
    else:
        logger.error(f'coser插件访问网络异常: {code}')
        message = MessageSegment.text('网络异常')
    return message
