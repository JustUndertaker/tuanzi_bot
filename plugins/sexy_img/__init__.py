import json

from httpx import RequestError, HTTPStatusError
from nonebot import on_command, logger
from nonebot.adapters.cqhttp import GroupMessageEvent, Bot, MessageSegment

from plugins.sexy_img.lolicon import fetch_lolicon_random_img

sexy_img = on_command("色图", aliases={"涩图", "不够色", "来一发", "再来点"}, priority=5, block=True)


@sexy_img.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = event.get_plaintext()
    # 当用户未传入任何关键字，则直接调用url请求随机图片
    if len(msg) == 0:
        try:
            '''
            {
              "title": "",
              "author": "",
              "url": ""
            }
            '''
            (title, author, url) = await fetch_lolicon_random_img()
            text = MessageSegment.text(f'标题: {title}\n画师: {author}\n地址: {url}\n')
            img = MessageSegment.image(url)
            await sexy_img.finish(text + img)
        except (RequestError, HTTPStatusError) as httpExc:
            logger.error(f'sexy插件访问网络异常: {httpExc}')
            await sexy_img.reject('网络异常')
        except json.JSONDecodeError as jsonExc:
            logger.error(f'sexy插件接口返回数据结构异常: {jsonExc}')
            await sexy_img.reject('返回异常')
        except Exception as e:
            logger.error(f'sexy插件异常: {e}')
            await sexy_img.reject('其余异常')
