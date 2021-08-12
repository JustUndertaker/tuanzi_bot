from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot import on_regex
from datetime import date
from nonebot.typing import T_State

from modules.user_info import User_Info
from modules.group_info import Group_Info
from utils.log import logger
import random

__plugin_name__ = '签到系统'
__plugin_usage__ = "普普通通的签到系统，每天0点重置\n命令：签到"

sign = on_regex(r"^签到$", permission=GROUP, priority=5, block=True)


@sign.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.user_id
    user_name = event.sender.nickname
    group_id = event.group_id

    # 更新记录
    await User_Info.append_or_update(user_id, group_id, user_name)
    await Group_Info.append_or_update(group_id)

    # 获取上次签到日期
    last_sign = await User_Info.get_last_sign(user_id, group_id)
    # 判断是否一致
    today = date.today()
    if today == last_sign:
        msg = MessageSegment.text('你今天已经签到了。')

    else:
        # 获取签到名次
        await Group_Info.sign_in_add(group_id)
        sign_num = await Group_Info.get_sign_nums(group_id)

        # 获取金币
        gold_add = random.randint(1, 100)
        await User_Info.change_gold(user_id, group_id, gold_add)
        user_gold = await User_Info.get_gold(user_id, group_id)

        # 好友度
        friendly_add = random.randint(1, 5)
        await User_Info.change_friendly(user_id, group_id, friendly_add)
        user_friendly = await User_Info.get_friendly(user_id, group_id)

        await User_Info.sign_in(user_id, group_id)

        msg = MessageSegment.at(user_id)
        msg += MessageSegment.text(f'\n本群第 {str(sign_num)} 位 签到完成')
        msg += MessageSegment.text(f'\n金币：+{str(gold_add)}(当前金币：{str(user_gold)})')
        msg += MessageSegment.text(f'\n好感度：+{str(friendly_add)}(当前好感度：{str(user_friendly)})')

    await sign.finish(msg)


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
