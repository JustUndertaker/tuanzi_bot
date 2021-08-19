
from typing import Union
from nonebot.adapters.cqhttp import MessageSegment

from .base import PluginManager
from modules.plugin_info import PluginInfo
from modules.group_info import GroupInfo


async def check_group_init(group_id: int) -> bool:
    '''
    :说明
        检查群是否注册

    :参数
        * group_id：QQ群号

    :返回
        * bool：是否注册
    '''
    return await GroupInfo.check_group_init(group_id)


async def check_plugin_status(module_name: str, group_id: int) -> Union[bool, None]:
    '''
    :说明
        查看插件状态

    :参数
        * module_name：插件模块名
        * group_id：QQ群号

    :返回
        * bool:插件状态
    '''
    return await PluginInfo.get_status(module_name, group_id)


async def plugin_init(group_id: int) -> None:
    '''
    :说明
        注册一个群的所有插件
    '''
    for plugin in PluginManager:
        module_name = plugin.module_name
        await PluginInfo.append_or_update(module_name, group_id)


async def change_plugin_status(plugin_name: str, group_id: int, status: bool) -> MessageSegment:
    '''
    :说明
        设置插件状态

    :参数
        * plugin_name：插件名
        * group_id：QQ群号
        * status：状态

    :返回
        * MessageSegment消息
    '''
    # 获取module_name
    module_name = None
    for plugin in PluginManager:
        if plugin.plugin_name == plugin_name:
            module_name = plugin.module_name
            break

    if module_name is not None:
        await PluginInfo.change_status(module_name, group_id, status)
        if status:
            msg = MessageSegment.text(f'插件[{plugin_name}]当前状态为：开启')
        else:
            msg = MessageSegment.text(f'插件[{plugin_name}]当前状态为：关闭')
    else:
        msg = MessageSegment.text(f'未找到插件[{plugin_name}]。')

    return msg
