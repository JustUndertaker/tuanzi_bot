
from utils.database import DB


'''
user_level表，用于管理用户权限等级



class User_info(DB.Base):
    # 表的名字:
    __tablename__ = 'user_level'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # 用户QQ号
    group_id = Column(Integer, nullable=False)  # 用户群号
    level = Column(Integer, default=0)  # 用户权限等级
'''
