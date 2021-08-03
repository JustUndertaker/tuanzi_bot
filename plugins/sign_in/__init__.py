from nonebot.adapters.cqhttp import Bot, Event, MessageSegment
from nonebot import on_regex
from nonebot.typing import T_State

from modules.user_info import User
from utils.log import logger


__plugin_name__ = '签到系统'
__plugin_usage__ = "普普通通的签到系统，每天0点重置\n命令：签到"

sign = on_regex(r"^签到$", priority=5, block=True)


@sign.handle()
async def _(bot: Bot, event: Event, state: T_State):
    user = User
    await sign.finish('签到成功')

# TODO:签到
'''
@user_id
头像图片
本群第 1 位 签到完成
金币：+72(上吉签)
今日宜：去叽叽庄找情缘
气运条：[----------]
您已累计签到 2 天
'''
