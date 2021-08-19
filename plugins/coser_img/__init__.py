import httpx
import re
from httpx import RequestError, HTTPStatusError
from nonebot import on_regex
from nonebot.exception import ActionFailed
from utils.log import logger
from nonebot.adapters.cqhttp import MessageSegment
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from nonebot.plugin import export

export = export()
export.plugin_name = 'COS'
export.plugin_usage = '获得好看的小姐姐\n命令：cos/coser'

_reg_pattern = r'^[cC][oO][sS](er)?$'
coser = on_regex(_reg_pattern, priority=5, block=True)
_rosysun_url = 'http://api.rosysun.cn/cos'


@coser.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # 只匹配cos纯指令(或coser，前三个字母不分大小写)，后续带任何字符都不作处理
    text = event.get_plaintext()
    matcher = re.match(_reg_pattern, text)
    if matcher is not None:
        message = _img_from_rosysun()
        try:
            # 由于图片可能无法访问，因此需要捕捉ActionFailed异常
            await coser.finish(message)
        except ActionFailed:
            await coser.finish('信息发送失败')


def _img_from_rosysun() -> MessageSegment:
    try:
        url = httpx.get(_rosysun_url).text
        message = MessageSegment.image(url)
        logger.info(f'COS插件发送: {message}')
    except (RequestError, HTTPStatusError) as httpExc:
        logger.error(f'COS插件访问网络异常: {httpExc}')
        message = MessageSegment.text('网络异常')
    except Exception as e:
        logger.error(f'COS插件异常: {e}')
        message = MessageSegment.text('其余异常')
    return message
