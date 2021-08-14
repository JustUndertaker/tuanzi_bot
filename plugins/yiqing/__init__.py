from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, MessageSegment, GroupMessageEvent
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import GROUP
import re

from .data_source import get_yiqing_card
from utils.log import logger
from .config import city_list

__plugin_name__ = '疫情查询'
__plugin_usage__ = '查询疫情帮助:\n\t对我说 疫情 省份/城市，我会回复疫情的实时数据\n\t示例: 疫情 温州'


yiqing = on_regex(r"([\u4e00-\u9fa5]+[疫情]$)|(^疫情 [\u4e00-\u9fa5]+$)", permission=GROUP,  priority=5, block=True)


@yiqing.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    message_str = event.get_plaintext()
    name = _get_name(message_str)

    province = ""
    city = None

    if name in city_list.keys():
        province = name
    else:
        for key in city_list.keys():
            if name in city_list.get(key):
                province = key
                city = name

    if province:
        msg = await get_yiqing_card(province, city)
        log = f'{event.sender.card}（{event.user_id}，{event.group_id}） - 查询疫情：{name}'
        logger.info(log)
    else:
        msg = MessageSegment.text('参数不对，不对！')

    await yiqing.finish(msg)


def _get_name(message_str: str) -> str:
    '''
    :说明
        匹配消息中的城市名称

    :参数
        * message_str：原始消息

    :返回
        * str：疫情city
    '''

    # 匹配前面
    args = re.search(r'[\u4e00-\u9fa5]+[疫情]$', message_str)
    if args != None:
        # 获得字符串
        loc = re.search('疫情', args.string).span()[0]
        args = args.string[0:loc]
        # 去除前缀
        head = re.search(r'(查一下)|(问一下)|(问问)|(想知道)|(查询)|(查查)', args)
        if head != None:
            loc = head.span()[1]
            args = args[loc:]
        return args
    else:
        # 匹配后面
        loc = re.search('疫情 ', message_str).span()[1]
        return message_str[loc:]