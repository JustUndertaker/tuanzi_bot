from sqlalchemy import Column, Integer, DATE
from utils.database import DB


'''
user_info表，用于管理整体用户数据
'''


class User_info(DB.Base):
    # 表的名字:
    __tablename__ = 'user_info'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # 用户QQ号
    group_id = Column(Integer, nullable=False)  # 用户群号
    gold = Column(Integer, default=0)  # 用户金币
    last_sign = Column(DATE)  # 上次签到日期
