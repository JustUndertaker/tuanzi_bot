from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot import on_regex
from nonebot.typing import T_State

from modules.user_info import User_Info
from utils.log import logger

__plugin_name__ = '签到系统'
__plugin_usage__ = "普普通通的签到系统，每天0点重置\n命令：签到"

sign = on_regex(r"^签到$", permission=GROUP, priority=5, block=True)


@sign.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.user_id
    group_id = event.group_id

    # 判断是否存在
    if not await User_Info.is_exist(user_id, group_id):
        await User_Info.append(user_id, group_id)
    # 设置签到日期
    await User_Info.sign_in(user_id, group_id)
    # 增加金币
    await User_Info.change_gold(user_id, group_id, 10)

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
