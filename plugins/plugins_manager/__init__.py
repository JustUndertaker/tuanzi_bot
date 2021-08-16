from nonebot.plugin import get_loaded_plugins
from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP

from nonebot.typing import T_State
import re

helpregex = r"([\u4E00-\u9FA5A-Za-z0-9_]+帮助$)|(^帮助 [\u4E00-\u9FA5A-Za-z0-9_]+$)"
help = on_regex(helpregex, permission=GROUP, priority=4, block=True)


@help.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):

    message_str = event.get_plaintext()
    name = _get_help_name(message_str)
    plugins_list = get_loaded_plugins()

    for plugin in plugins_list:
        # 获取插件名称
        if plugin.name == 'plugins_manager':
            continue
        try:
            plugin_name = plugin.export['plugin_name']
            if name == plugin_name:
                plugin_usage = plugin.export['plugin_usage']
                break
        except:
            pass

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
    if args != None:
        # 获得字符串
        loc = re.search('帮助', args.string).span()[0]
        args = args.string[0:loc]
        # 去除前缀
        head = re.search(r'(查一下)|(问一下)|(问问)|(想知道)|(查询)|(查查)', args)
        if head != None:
            loc = head.span()[1]
            args = args[loc:]
        return args
    else:
        # 匹配后面
        loc = re.search('帮助 ', message_str).span()[1]
        return message_str[loc:]
