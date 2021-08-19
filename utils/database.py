from peewee import SqliteDatabase
from configs.pathConfig import DATABASE_PATH
from modules.user_info import UserInfo
from modules.group_info import GroupInfo
from modules.user_level import UserLevel
from modules.plugin_info import PluginInfo

from nonebot.log import logger


def database_init():
    '''
    初始化建表
    '''
    logger.info('正在注册数据库')
    table_list = [
        UserInfo,
        GroupInfo,
        UserLevel,
        PluginInfo
    ]
    DB = SqliteDatabase(DATABASE_PATH)
    DB.connect()
    DB.create_tables(table_list)
    logger.info('数据库注册完成')
