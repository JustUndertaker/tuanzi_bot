from configs.pathConfig import DATABASE_PATH
from .log import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


class DBclass():
    def __init__(self):
        db_name = 'data.db'
        db_path = DATABASE_PATH+db_name
        self.DB = create_engine(f'sqlite:///{db_path}?check_same_thread=False')
        self.Base = declarative_base()
        logger.info(f'数据库初始化完成……')

    def get_session(self):
        '''
        返回一个seesion链接，记得关闭
        '''
        session = scoped_session(sessionmaker(bind=self.DB))
        return session


# 全局数据库对象
DB = DBclass()
