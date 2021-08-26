import datetime
import random
from typing import Union
from modules.duel_history import DuelHistory


def get_latest_duel(group_id: int) -> Union[DuelHistory, None]:
    """
    :说明：
        根据群号获取最近一场决斗记录

    :参数
        * group_id：QQ群号

    :返回
        * DuelHistory：俄罗斯轮盘决斗记录
        * None：不存在记录
    """
    r = DuelHistory\
        .select()\
        .where(DuelHistory.group_id == group_id)\
        .order_by(DuelHistory.start_time.desc())
    if len(r) <= 0:
        return None
    return r[0]


def get_latest_can_handle_duel(group_id: int) -> Union[DuelHistory, None]:
    """
    :说明：
        根据群号获取最近一场可被接受/拒绝的决斗记录

    :参数
        * group_id：QQ群号

    :返回
        * DuelHistory：俄罗斯轮盘决斗记录
        * None：不存在记录
    """
    r = DuelHistory\
        .select()\
        .where(DuelHistory.group_id == group_id, DuelHistory.state == 0)\
        .order_by(DuelHistory.start_time.desc())
    if len(r) <= 0:
        return None
    return r[0]


def get_latest_can_shot_duel(group_id: int) -> Union[DuelHistory, None]:
    """
    :说明：
        根据群号获取最近一场决斗中的记录

    :参数
        * group_id：QQ群号

    :返回
        * DuelHistory：俄罗斯轮盘决斗记录
        * None：不存在记录
    """
    r = DuelHistory\
        .select()\
        .where(DuelHistory.group_id == group_id, DuelHistory.state == 1)\
        .order_by(DuelHistory.start_time.desc())
    if len(r) <= 0:
        return None
    return r[0]


def insert_duel(
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
        * DuelHistory：俄罗斯轮盘决斗记录
        * None：不存在记录
    """
    DuelHistory.create(
        group_id=group_id,
        player1_id=player1,
        player2_id=player2,
        in_turn=player1,
        wager=wager,
        state=0,
    )


def duel_accept(duel: DuelHistory):
    # 每枪中弹概率
    p = random.uniform(0, 0.7)
    # 生成弹闸列表
    bullet_list = ['1' if r > p else '0' for r in [random.uniform(0, 1) for _ in range(0, 7)]]
    # 默认是player1开首枪
    duel.in_turn = duel.player1_id
    duel.bullet = ','.join(bullet_list)
    duel.probability = p
    duel.state = 1
    duel.last_shot_time = datetime.datetime.now()
    duel.save()


def duel_end(duel: DuelHistory):
    duel.state = 2
    duel.end_time = datetime.datetime.now()
    duel.save()


def duel_denied(duel: DuelHistory):
    duel.state = -1
    duel.save()


def duel_shot(duel: DuelHistory) -> bool:
    """
    开枪，同时更换开枪选手
    True -> 被击中
    False -> 未被击中
    """
    result = duel.current_bullet
    duel.order = duel.order + 1
    duel.switch()
    duel.last_shot_time = datetime.datetime.now()
    duel.save()
    return result


def duel_switch(duel: DuelHistory):
    duel.switch()
    duel.last_shot_time = datetime.datetime.now()
    duel.save()
