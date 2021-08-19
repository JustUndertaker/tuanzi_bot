from nonebot import get_driver
from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment, GROUP_OWNER, GROUP_ADMIN
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.message import run_preprocessor
from nonebot.plugin import Matcher
from nonebot.permission import SUPERUSER

from nonebot.typing import T_State
import re
import os
from typing import Union
from .base import manager_init, PluginManager
from nonebot.exception import IgnoredException
from .data_source import check_plugin_status, plugin_init, change_plugin_status, check_group_init


# 获取本模块名
_, self_module = os.path.split(os.path.split(__file__)[0])

# ==============插件管理器注册==============
driver = get_driver()
driver.on_startup(manager_init)


@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    插件管理预处理函数，只处理群消息
    '''
    # 获取群号
    group_id = event.group_id
    # 获取插件模块名
    module_name = matcher.plugin_name

    # 判断是否注册
    is_init = await check_group_init(group_id)

    # 判断是否跳过本插件
    if module_name == self_module:
        if is_init or (state['_matched'] == '注册'):
            return

    # 鉴权函数
    status = await check_plugin_status(module_name, group_id)

    if status is None:
        raise IgnoredException(f'[{group_id}]群未注册。')
    elif not status:
        raise IgnoredException(f'[{module_name}]插件未开启。')

# =============插件帮助===================
helpregex = r"([\u4E00-\u9FA5A-Za-z0-9_]+帮助$)|(^帮助 [\u4E00-\u9FA5A-Za-z0-9_]+$)"
help = on_regex(helpregex, permission=GROUP, priority=4, block=True)


@help.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):

    message_str = event.get_plaintext()
    name = _get_help_name(message_str)

    plugin_usage = None
    for plugin in PluginManager:
        # 获取插件名称
        if plugin.plugin_name == name:
            plugin_usage = plugin.plugin_usage
            break

    if plugin_usage is None:
        msg = MessageSegment.text(f'未找到插件[{name}]，看看参数是否正确。')
    else:
        msg = MessageSegment.text(plugin_usage)

    await help.finish(msg)


def _get_help_name(message_str: str) -> str:
    '''
    :说明
        * 获取帮助的插件名称
    '''
    # 匹配前面
    args = re.search(r'[\u4E00-\u9FA5A-Za-z0-9_]+[帮助]$', message_str)
    if args is not None:
        # 获得字符串
        loc = re.search('帮助', args.string).span()[0]
        args = args.string[0:loc]
        # 去除前缀
        head = re.search(r'(查一下)|(问一下)|(问问)|(想知道)|(查查)', args)
        if head is not None:
            loc = head.span()[1]
            args = args[loc:]
        return args
    else:
        # 匹配后面
        loc = re.search('帮助 ', message_str).span()[1]
        return message_str[loc:]


update = on_regex(r"^注册$", permission=SUPERUSER, priority=2, block=False)


@update.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    '''
    管理员注册群信息，和后面的签到是同一个命令
    '''
    # 群id
    group_id = event.group_id
    # 注册
    await plugin_init(group_id)

changeregex = r'^设置 [\u4E00-\u9FA5A-Za-z0-9_]+ [开|关]$'
change = on_regex(changeregex, permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN, priority=2, block=False)


@change.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    text = event.get_plaintext()
    try:
        plugin_name, status = _get_change_params(text)
        msg = await change_plugin_status(plugin_name, group_id, status)
    except Exception:
        msg = MessageSegment.text('参数正确吗？检查一下。')

    await change.finish(msg)


def _get_change_params(text: str) -> tuple[str, bool]:
    '''
    :说明
        从原始消息中解析出插件名和开关状态

    :参数
        原始消息

    :返回
        * plugin_name：插件名
        * status：开关状态
    '''
    text_list = text.split(' ')
    try:
        plugin_name = text_list[1]
        _status = text_list[2]
        if _status == '开':
            status = True
        elif _status == '关':
            status = False
        else:
            raise Exception
    except Exception:
        raise Exception
    return plugin_name, status
