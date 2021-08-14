import json

import httpx
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment, Message
from nonebot.log import logger
from httpx import HTTPStatusError, RequestError
from nonebot.typing import T_State

_plugin_name = '识番'
_api = 'https://api.trace.moe/search'
whatanime = on_command("识番", priority=5, block=True)


@whatanime.args_parser
@whatanime.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    """
    通过whatanime的api以图识番
    """
    message = event.message
    if isinstance(message, list) & len(message) >= 1:
        # 获取消息中的第一张图片(如果有)
        first_message: MessageSegment = message[0]
        state['img_url'] = first_message.data.get('url', None)


@whatanime.got('img_url', prompt='图呢?')
async def _(bot: Bot, event: MessageEvent, state: T_State):
    url = state.get('img_url', '')
    if len(url) <= 0:
        return
    await whatanime.send('正在识别...')
    try:
        j = httpx.get(_api, params={'url': url}).json()
        error = j.get('error', '')
        if len(error) > 0:
            await whatanime.send(f'错误信息: {error}')
        else:
            result = j.get('result', [])
            for item in result:
                await whatanime.send(_parse_to_message(item))
    except (RequestError, HTTPStatusError) as httpExc:
        logger.error(f'{_plugin_name}插件访问网络异常: {httpExc}')
        await whatanime.reject('网络异常')
    except json.JSONDecodeError as jsonExc:
        logger.error(f'{_plugin_name}插件接口返回数据结构异常: {jsonExc}')
        await whatanime.reject('返回异常')
    except Exception as e:
        logger.error(f'{_plugin_name}插件异常: {e}')
        await whatanime.reject('其余异常')
    finally:
        await whatanime.finish('识别完毕')


# 将搜索结果包装成消息
def _parse_to_message(item) -> Message:
    name = f'名称: {item.get("filename", "")}'
    episode = f'集数: {item.get("episode", "")}'
    similarity = f'相似度: {round(item.get("similarity", ""), 4) * 100}%'
    second = f'从第{item.get("from", "")}秒到第{item.get("to", "")}秒'
    snapshot = '截图: '
    url = item.get("image", "")
    text = MessageSegment.text(str.join('\n', [name, episode, similarity, second, snapshot]))
    img = MessageSegment.image(url)
    return text + img