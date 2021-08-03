import json
import random

import regex
from httpx import RequestError, HTTPStatusError
from nonebot import on_regex
from utils.log import logger
from nonebot.adapters.cqhttp import MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from plugins.sexy_img.lolicon import fetch_lolicon_random_img


_reg_pattern = r'^[色|涩]图$'
sexy_img = on_regex(_reg_pattern, priority=5, block=True)


# 注意所有获取图片的api，其返回格式必须符合
# title author url
_random_api = [
    fetch_lolicon_random_img
]


@sexy_img.handle()
async def _(bot: Bot, event: Event, state: T_State):
    text = event.get_plaintext()
    matcher = regex.match(_reg_pattern, text)
    # 当前色图插件只支持纯指令(避免和搜/识图插件的指令混淆)
    if matcher is not None:
        try:
            api = _get_random_api()
            (title, author, url) = await api()
            text = MessageSegment.text(f'标题: {title}\n画师: {author}\n地址: {url}\n')
            img = MessageSegment.image(url)
            logger.info(f'sexy插件发送: {text + img}')
            message = text + img
        except (RequestError, HTTPStatusError) as httpExc:
            logger.error(f'sexy插件访问网络异常: {httpExc}')
            message = MessageSegment.text('网络异常')
        except json.JSONDecodeError as jsonExc:
            logger.error(f'sexy插件接口返回数据结构异常: {jsonExc}')
            message = MessageSegment.text('返回异常')
        except Exception as e:
            logger.error(f'sexy插件异常: {e}')
            message = MessageSegment.text('其余异常')
        await sexy_img.finish(message)


# 返回随机获取图片的随机一个api
def _get_random_api():
    api = _random_api[random.randint(0, len(_random_api) - 1)]
    return api
