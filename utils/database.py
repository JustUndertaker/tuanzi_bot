from peewee import SqliteDatabase
from configs.pathConfig import DATABASE_PATH
from modules.user_info import UserInfo
from modules.group_info import GroupInfo
from modules.user_level import UserLevel


def init():
    '''
    初始化建表
    '''
    table_list = [
        UserInfo,
        GroupInfo,
        UserLevel
    ]
    DB = SqliteDatabase(DATABASE_PATH)
    DB.connect()
    DB.create_tables(table_list)
