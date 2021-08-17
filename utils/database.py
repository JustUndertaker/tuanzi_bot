from peewee import SqliteDatabase
from configs.pathConfig import DATABASE_PATH
from modules.user_info import UserInfo
from modules.group_info import Group_Info
from modules.user_level import User_Level


def init():
    '''
    初始化建表
    '''
    table_list = [
        UserInfo,
        Group_Info,
        User_Level
    ]
    DB = SqliteDatabase(DATABASE_PATH)
    DB.connect()
    DB.create_tables(table_list)
