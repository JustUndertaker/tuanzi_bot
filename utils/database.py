from peewee import SqliteDatabase
from configs.pathConfig import DATABASE_PATH
from modules.user_info import User_Info


def init():
    '''
    初始化建表
    '''
    table_list = [
        User_Info,
    ]
    DB = SqliteDatabase(DATABASE_PATH)
    DB.connect()
    DB.create_tables(table_list)
