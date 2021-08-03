from sqlalchemy import Column, Integer, Boolean
from utils.database import DB

'''
group_info表，用于管理注册的群组信息，和机器人全局开关
'''


class User_info(DB.Base):
    # 表的名字:
    __tablename__ = 'group_info'

    # 表的结构:
    group_id = Column(Integer, primary_key=True, nullable=False)  # 用户群号
    sign_nums = Column(Integer, default=0)  # 签到人数
    status = Column(Boolean, default=True)  # 机器人开关

    @classmethod
    def reset_sign_nums(cls) -> int:
        '''
        :说明
            重置所有群的签到人数，一般0点触发

        :返回
            * 0：正常返回
            * 1：数据库链接错误
        '''
        data = {'sign_nums': 0}
        session = DB.get_session()
        group_list = session.query(cls).all()
        try:
            group_list.update(data)
            session.commit()
            session.close()
            return 0

        except:
            return 1

    @classmethod
    def add_sign_in(cls, group_id: int) -> int:
        '''
        :说明
            增加一个群的签到数量

        :参数
            * group_id：QQ群号

        :返回
            * 0：操作成功
            * 1：数据库链接错误
            * 2：未注册群信息
        '''

        session = DB.get_session()
        # 获取签到数
        record = session.query(cls).filter(cls.group_id == group_id).first()
        # 判断是否注册群信息
        if record is None:
            return 2

        sign_num = record.sign_nums+1
        data = {'sign_nums': sign_num}

        try:
            record.update(data)
            session.commit()
            session.close()
            return 0
        except:
            return 1

    @classmethod
    def set_status(cls, group_id: int, status: bool) -> int:
        '''
        :说明
            设置机器人群全局开关状态

        :参数
            * group_id：QQ群号
            * status：开关状态

        :返回
            * 0：操作成功
            * 1：数据库链接错误
            * 2：未注册群组信息
        '''
        session = DB.get_session()
        # 获取签到数
        record = session.query(cls).filter(cls.group_id == group_id).first()
        # 判断是否注册群信息
        if record is None:
            return 2

        data = {'status': status}

        try:
            record.update(data)
            session.commit()
            session.close()
            return 0
        except:
            return 1
