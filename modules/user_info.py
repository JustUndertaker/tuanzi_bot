from sqlalchemy import Column, Integer, DATE
from utils.database import DB
from datetime import date


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
    friendly = Column(Integer, default=0)  # 用户好感度
    last_sign = Column(DATE)  # 上次签到日期

    @classmethod
    def get_gold(cls, user_id: int, group_id: int) -> int:
        '''
        :说明：
            获取用户的金币数量

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * 金币数量
        '''
        session = DB.get_session()
        # 获取金币
        record = session.query(cls).filter(cls.group_id == group_id, cls.user_id == user_id).first()
        session.close()
        return record.gold

    @classmethod
    def get_friendly(cls, user_id: int, group_id: int) -> int:
        '''
        :说明：
            获取用户的好感度

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * 好感度
        '''
        session = DB.get_session()
        # 获取金币
        record = session.query(cls).filter(cls.group_id == group_id, cls.user_id == user_id).first()
        session.close()
        return record.friendly

    @classmethod
    def get_last_sign(cls, user_id: int, group_id: int) -> date:
        '''
        :说明：
            获取用户的上次签到日期

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * date:上次签到日期
        '''
        session = DB.get_session()
        # 获取金币
        record = session.query(cls).filter(cls.group_id == group_id, cls.user_id == user_id).first()
        lastdate = record.last_sign
        if lastdate is None:
            return None
        # TODO date类型转换
        session.close()
        return lastdate

    @classmethod
    def sign_in(cls, user_id: int, group_id: int):
        '''
        :说明：
            签到

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
        '''
        nowday = date.today()
        session = DB.get_session()
        data = {'last_sign', nowday}
        record = session.query(cls).filter(cls.group_id == group_id, cls.user_id == user_id).first()
        record.update(data)
        session.commit()
        session.close()
