from peewee import *
from datetime import datetime
from configs.pathConfig import DATABASE_PATH

'''
user_info表，用于管理整体用户数据
'''

DB = SqliteDatabase(DATABASE_PATH)


class User_Info(Model):

    # 表的结构
    user_id = IntegerField(verbose_name='用户QQ号', null=False)
    group_id = IntegerField(verbose_name='QQ群号', null=False)
    gold = IntegerField(verbose_name='金币数', default=0)
    friendly = IntegerField(verbose_name='好感度', default=0)
    last_sign = DateField(verbose_name='上次签到日期', null=True)

    class Meta:
        table_name = 'user_info'
        database = DB

    @classmethod
    async def get_friendly(cls, user_id: int, group_id: int) -> int:
        '''
        :说明：
            获取用户的好感度

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * 好感度
        '''
        record = cls.get((cls.user_id == user_id) & (cls.group_id == group_id))
        return record.friendly

    @classmethod
    async def get_gold(cls, user_id: int, group_id: int) -> int:
        '''
        :说明：
            获取用户的金币

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * 好感度
        '''
        record = cls.get((cls.user_id == user_id) & (cls.group_id == group_id))
        return record.gold

    @classmethod
    async def get_last_sign(cls, user_id: int, group_id: int) -> datetime:
        '''
        :说明：
            获取用户的上次签到日期

        :参数
            * user_id：用户QQ
            * group_id：QQ群号

        :返回
            * date:上次签到日期
        '''
        record = cls.get((cls.user_id == user_id) & (cls.group_id == group_id))
        return record.last_sign

    @classmethod
    async def sign_in(cls, user_id: int, group_id: int) -> None:
        '''
        :说明：
            签到

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
        '''
        today = datetime.today()
        record = cls.get((cls.user_id == user_id) & (cls.group_id == group_id))
        record.last_sign = today
        record.save()

    @classmethod
    async def append(cls, user_id: int, group_id: int) -> None:
        '''
        :说明
            增加一条记录

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
        '''
        try:
            record = cls.get((cls.user_id == user_id) & (cls.group_id == group_id))
        except:
            cls.create(user_id=user_id, group_id=group_id)

    @classmethod
    async def delete(cls, user_id: int, group_id: int) -> None:
        '''
        :说明
            删除一条记录

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
        '''
        record = cls.get((cls.user_id == user_id) & (cls.group_id == group_id))
        record.delete_instance()

    @classmethod
    async def change_gold(cls, user_id: int, group_id: int, num: int) -> None:
        '''
        :说明
            改变金币数量

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
            * num：改变金币数量
        '''
        record = cls.get((cls.user_id == user_id) & (cls.group_id == group_id))
        record.gold = record.gold+num
        record.save()

    @classmethod
    async def is_exist(cls, user_id: int, group_id: int) -> bool:
        '''
        :说明
            判断是否存在该记录

        :参数
            * user_id：用户QQ
            * group_id：QQ群号
        '''
        try:
            record = cls.get((cls.user_id == user_id) & (cls.group_id == group_id))
            return True
        except:
            return False
