from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.adapters.cqhttp.permission import GROUP

from nonebot.typing import T_State
from utils.log import logger
from .data_source import get_chat_reply


__plugin_name__ = '智能闲聊'
__plugin_usage__ = "普普通通的闲聊\n命令：@robot闲聊内容"

chat = on_message(rule=to_me(), permission=GROUP, priority=8, block=True)


@chat.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    自动根据确定API
    '''
    # 获得聊天内容
    text = event.get_plaintext()
    flag = True
    log = f'{event.sender.card}（{event.user_id}，{event.group_id}） - 开启闲聊：{text}'
    logger.info(log)
    try:
        msg = await get_chat_reply(text)
    except:
        log = f'闲聊失败了……'
        logger.info(log)
        flag = False

    if flag:
        await chat.finish(msg)
    else:
        await chat.finish()
