
from utils.database import DB

'''
group_info表，用于管理注册的群组信息，和机器人全局开关



class User_info(DB.Base):
    # 表的名字:
    __tablename__ = 'group_info'

    # 表的结构:
    group_id = Column(Integer, primary_key=True, nullable=False)  # 用户群号
    sign_nums = Column(Integer, default=0)  # 签到人数
    status = Column(Boolean, default=True)  # 机器人开关
'''
