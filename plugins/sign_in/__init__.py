from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot import on_regex
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from utils.utils import scheduler, get_bot

from .data_source import get_sign_in, reset, update_info
from utils.log import logger
from nonebot.plugin import export

export = export()
export.plugin_name = '签到'
export.plugin_usage = '普普通通的签到系统，每天0点重置\n命令：签到'

sign = on_regex(r"^签到$", permission=GROUP, priority=5, block=True)


@sign.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.user_id
    user_name = event.sender.card
    if user_name == '':
        user_name = event.sender.nickname
    group_id = event.group_id

    msg = await get_sign_in(user_id, group_id, user_name)
    await sign.finish(msg)

update = on_regex(r"^注册$", permission=SUPERUSER, priority=5, block=True)


@update.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    bot = get_bot()
    group_id = event.group_id
    member_list = await bot.get_group_member_list(group_id=group_id)
    msg = await update_info(group_id, member_list)
    log = f'（{event.group_id}）管理员更新信息'
    logger.info(log)
    await update.finish(msg)


# 定时任务
@scheduler.scheduled_job("cron", hour=0, minute=0)
async def _():
    group_list = await reset()
    bot = get_bot()
    for group_id in group_list:
        try:
            await bot.send_group_msg(group_id=group_id, message='又是元气满满的一天呢~')
        except Exception:
            log = f'（{group_id}）群被禁言了，无法发送晚安……'
            logger.warning(log)
