from nonebot import require
import nonebot

scheduler = require('nonebot_plugin_apscheduler').scheduler


def get_bot():
    return list(nonebot.get_bots().values())[0]
