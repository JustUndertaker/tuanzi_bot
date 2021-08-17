import nonebot
from nonebot import require

# 全局定时器对象
scheduler = require('nonebot_plugin_apscheduler').scheduler


def get_bot():
    '''
    全局获取bot对象
    '''
    return list(nonebot.get_bots().values())[0]
