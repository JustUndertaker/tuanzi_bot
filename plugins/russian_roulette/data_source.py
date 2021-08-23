import datetime
import random
import time
from typing import Union
from peewee import *
from configs.pathConfig import DATABASE_PATH

_TIMEOUT = 60 * 1000
_TEN_MILLION: int = 10000000


class DuelHistory(Model):
    """
    记录俄罗斯轮盘的决斗历史，由于每个群同一时间只能有一个决斗存在，因此只需要通过group_id定位即可
    state取值:
    0 -> 决斗邀请阶段
    1 -> 对决开始
    -1 -> 对决被拒绝
    2 -> 决斗结束(无论超时还是被结算)

    in_turn为当前开枪的id
    bullet为8位数，首位为当前第几颗子弹，后7位为弹闸的数字化，1代表有子弹，0代表无子弹
    """
    # 表的结构
    group_id = IntegerField(verbose_name='QQ群号', null=False)
    player1_id = IntegerField(verbose_name='挑战者', default='')
    player2_id = IntegerField(verbose_name='被挑战者', default=0)
    wager = IntegerField(verbose_name='赌注', default=0)
    state = IntegerField(verbose_name='状态', default=0)
    in_turn = IntegerField(verbose_name='裁决者')
    # 为啥要用字符串来记录，因为python的二进制处理实在太蛋疼了
    bullet = CharField(verbose_name='弹闸', default=0)
    order = IntegerField(verbose_name='子弹', default=0)
    probability = IntegerField(verbose_name='中枪概率', default=0)
    last_shot_time = IntegerField(verbose_name='上次开枪时间', default=0)
    start_time = DateTimeField(verbose_name='累计签到次数', default=datetime.datetime.now())
    end_time = DateTimeField(verbose_name='上次签到日期', null=True)

    class Meta:
        table_name = 'duel_history'
        database = SqliteDatabase(DATABASE_PATH)

    def can_be_accept(self):
        """
        决斗是否可以被接受
        """
        return self.state == 0

    def active(self) -> bool:
        """
        决斗是否有效，有效意味着可以进行"接受"、"拒绝"等操作
        """
        return self.state == 0 | self.state == 1

    def in_duel(self):
        """
        是否在决斗过程中
        """
        return self.state == 1

    @property
    def current_bullet(self) -> bool:
        """
        获取当前弹闸中子弹，True为有子弹，False为空枪
        """
        order = int(self.order)
        bullet_str = str(self.bullet).split(',')
        return bullet_str[order] == '1'

    @property
    def visual_bullet(self) -> str:
        return str(self.bullet).replace('0', '_')

    def clearing(self):
        """
        结算，根据当前状态返回最后(胜者, 败者)id
        """
        temp_order = self.order
        temp_shot_id = self.in_turn
        bullet_str = str(self.bullet).split(',')[temp_order:]
        for bullet in bullet_str:
            if bullet == '1':
                loser = temp_shot_id
                winner = self.player2_id if loser == self.player1_id else self.player1_id
                return winner, loser
            temp_shot_id = self.player1_id if temp_shot_id == self.player1_id else self.player2_id
        return None, None

    def can_be_shot(self):
        return self.order < 8

    def expired(self) -> bool:
        current_time = time.time()
        if self.state == 0:
            return (current_time - self.start_time) > _TIMEOUT
        elif self.state == 1:
            return (current_time - self.last_shot_time) > _TIMEOUT
        else:
            return True

    @property
    def another(self):
        """
        返回当前开枪的另一位玩家id，如当前轮到player1开枪，则返回player2的id
        """
        return self.player1_id if self.in_turn == self.player2_id else self.player2_id

    def switch(self):
        self.in_turn = self.player1_id if self.in_turn == self.player1_id else self.player2_id

    def _state_to_string(self):
        if self.state == 0:
            return '决斗邀请'
        elif self.state == 1:
            return '决斗开始'
        elif self.state == 2:
            return '决斗结束'
        elif self.state == -1:
            return '决斗被拒绝'
        else:
            return '非法状态'

    def __str__(self):
        return f'groupId: {self.group_id}\n' \
               f'player1Id: {self.player1_id}\n' \
               f'player2Id: {self.player2_id}\n' \
               f'赌注: {self.wager}\n' \
               f'决斗状态: {self._state_to_string()}\n' \
               f'当前开枪用户: {self.in_turn}\n' \
               f'子弹可视图: {self.visual_bullet}\n' \
               f'第几颗子弹: {self.order}\n' \
               f'中枪概率: {self.probability}\n' \
               f'上次开枪时间: {self.last_shot_time}\n' \
               f'开始时间: {self.start_time}\n' \
               f'结束时间: {self.end_time}\n'


async def get_latest_duel(group_id: int) -> Union[DuelHistory, None]:
    """
    :说明：
        根据群号获取最近一场决斗记录

    :参数
        * group_id：QQ群号

    :返回
        * RussianBullet：俄罗斯轮盘决斗记录
        * None：不存在记录
    """
    return DuelHistory.get_or_none(DuelHistory.group_id == group_id)


async def insert_duel(
        group_id: int,
        player1: int,
        player2: int,
        wager: int,
):
    """
    :说明：
        插入一条新的决斗记录

    :参数
        * group_id：QQ群号
        * player1：决斗者QQ号
        * player2：被决斗者QQ号
        * wager：赌注

    :返回
        * RussianBullet：俄罗斯轮盘决斗记录
        * None：不存在记录
    """
    await DuelHistory.create(
        group_id=group_id,
        player1=player1,
        player2=player2,
        wager=wager,
        state=0,
    )


async def duel_accept(duel: DuelHistory):
    # 每枪中弹概率
    p = random.uniform(0, 1)
    # 生成弹闸列表
    bullet_list = ['1' if r > p else '0' for r in [random.uniform(0, 1) for _ in range(0, 7)]]
    # 默认是player1开首枪
    duel.in_turn = duel.player1_id
    duel.bullet = ','.join(bullet_list)
    duel.probability = p
    duel.state = 1
    duel.last_shot_time = time.time()
    await DuelHistory.update(duel)


async def duel_end(duel: DuelHistory):
    duel.state = 2
    duel.end_time = datetime.datetime.now()
    await DuelHistory.update(duel)


async def duel_denied(duel: DuelHistory):
    duel.state = -1
    await DuelHistory.update(duel)


async def duel_shot(duel: DuelHistory) -> bool:
    """
    开枪，同时更换开枪选手
    True -> 被击中
    False -> 未被击中
    """
    duel.order = duel.order + 1
    duel.switch()
    duel.last_shot_time = time.time()
    await DuelHistory.update(duel)
    return duel.current_bullet


async def duel_switch(duel: DuelHistory):
    duel.switch()
    duel.last_shot_time = time.time()
    await DuelHistory.update(duel)
