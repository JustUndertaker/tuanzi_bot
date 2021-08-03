from configs.pathConfig import DATABASE_PATH
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from nonebot.log import logger


class DBclass():

    def __init__(self):
        '''
        数据库初始化
        '''
        db_name = 'data.db'
        db_path = DATABASE_PATH+db_name
        db_uri = f'sqlite:///{db_path}?check_same_thread=False'
        self.DB = create_engine(db_uri)
        self.Base = declarative_base(bind=self.DB)

    def init(self):
        self.Base.metadata.create_all()
        logger.info('数据库初始化成功……')

    def get_session(self):
        '''
        返回一个seesion链接，记得关闭
        '''
        session = sessionmaker(bind=self.DB)()
        return session

    def shutdown(self):
        '''
        关闭数据库
        '''
        pass


# 全局数据库对象
DB = DBclass()
