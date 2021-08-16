import time

from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import GROUP, GroupMessageEvent, Message, MessageSegment
from nonebot.typing import T_State

from utils.log import logger
from .sentence import challenge, group_challenge, random_sentence, accept_challenge

_plugin_name = '俄罗斯轮盘'
__plugin_usage__ = "装弹[金币][at](指定决斗对象，为空则所有群友都可接受决斗)"
russian_roulette = on_command('俄罗斯轮盘', aliases={'装弹', '俄罗斯转盘'}, permission=GROUP, priority=5, block=True)
_accept = on_command('接受', aliases={'接受决斗', '接受挑战'}, permission=GROUP, priority=5, block=True)
_refuse = on_command('拒绝', aliases={'拒绝决斗', '拒绝挑战'}, permission=GROUP, priority=5, block=True)


"""
player1为发起决斗者
player2为被决斗者
gold为决斗要花费的金币
started_time为当前决斗发起时间
_last_active_time为上一个动作的发起时间(用于开枪及结算)
"""
_player1: int = -1
_player2: int = -1
_gold: int = 0
_started_time: int = 0
_last_active_time: int = 0
# 决斗超时限制
_TIMEOUT = 60


@russian_roulette.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    global _player1, _player2, _gold, _started_time
    message = event.message
    if len(message) <= 0:
        await russian_roulette.finish(__plugin_usage__)
        return
    # 若此前已经存在决斗，检查其是否超时
    current_time = time.time()
    # 若超时则直接开始新一轮决斗(重置所有参数)
    if (current_time - _started_time) > _TIMEOUT:
        # 若前一轮决斗超时则重置所有属性(由于_started_time默认为0，则无决斗时仍会走该逻辑)
        _reset()
        # 记录挑战时间，若超时且未有响应则取消当前决斗，决斗过程中有超时未响应行为则进入结算
        _started_time = current_time
    t_player1 = event.sender.user_id
    # 检查当前是否已经存在决斗
    if _player1 != -1:
        if _player1 == t_player1:
            await russian_roulette.finish('请先完成当前决斗')
        else:
            await russian_roulette.finish('请勿打扰别人神圣的决斗，丨')
        return
    # 记录挑战者id
    _player1 = t_player1
    # 获取第一个被@的人作为被挑战者
    _player2 = -1
    for item in message:
        if item.type == 'at':
            _player2 = int(item.data.get('qq', -1))
            break
    # 命令后第一个参数必须为数字，作为决斗花费的金额
    _gold = -1
    gold_message = message[0]
    if gold_message.is_text:
        message_text = str(gold_message).strip()
        if message_text.isdigit():
            _gold = int(gold_message.__str__())
    if _gold < 0:
        await russian_roulette.finish('咋地，决斗完还想倒吸钱啊?')
        return
    # TODO 检查双方(如player2未被指定则只检测player1)是否有足够金币迎战
    _player1_gold = 0

    # 若无指定被决斗者，则所有群员都可响应这场决斗
    if _player2 == -1:
        await russian_roulette.finish(random_sentence(group_challenge))
        return
    # 不能自己和自己决斗
    if _player2 == _player1:
        _reset()
        await russian_roulette.finish(f'珍爱生命，不要自残', at_sender=True)
    # 也不允许向机器人发起决斗
    elif _player2 == event.self_id:
        _reset()
        await russian_roulette.finish('敢向裁判挑战? 不怕我毙了你嘛')
    else:
        # 向被决斗人发送at消息
        random_s = random_sentence(challenge)
        message = Message(f'{MessageSegment.at(_player2)}{random_s}')
        await russian_roulette.finish(message)


@_accept.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    global _player1, _player2, _started_time
    # 决斗可能因超时被取消(或根本无发生过任何决斗)
    if _player1 == -1:
        await _accept.finish('当前无任何决斗，你接受个什么劲儿')
        return
    accept_id = event.user_id
    current_time = time.time()
    # 检测此前是否有指定人选
    if _player2 == -1 or _player2 == accept_id:
        # 检测决斗是否超时
        if (current_time - _started_time) > _TIMEOUT:
            _reset()
            await _accept.finish('该场决斗已经超时，请重新发起')
            return
        _player2 = accept_id
        # TODO 检测player2是否有足够金币进行决斗
        # 进入下一阶段
        random_s = random_sentence(accept_challenge)
        message = Message(f'{MessageSegment.at(_player2)}{random_s}{MessageSegment.at(_player1)}')
        await _accept.send(message)
        await _accept.finish('请通过[开枪]来把握自己的命运')
    else:
        await _accept.finish('和你无关，一边玩泥巴去!')


@_refuse.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    global _player1, _player2, _gold, _started_time
    # 决斗可能因超时被取消(或根本无发生过任何决斗)
    if _player1 == -1:
        await _refuse.finish('当前无任何决斗，你怂个啥哦')
        return
    refuse_id = event.user_id
    current_time = time.time()
    if _player2 == -1:
        await _refuse.finish('这场决斗面向所有人，不用站出来认怂')
        return
    if _player2 == refuse_id:
        # 检测决斗是否超时
        if (current_time - _started_time) > _TIMEOUT:
            _reset()
            message = Message(f'尽管决斗已经超时，但{MessageSegment.at(_player2)}还是向我们展示了他的胆小')
            await _refuse.finish(message)
            return
        _reset()
        message = Message(f'卑微的{MessageSegment.at(_player2)}拒绝了应用的{MessageSegment.at(_player1)}')
        await _refuse.finish(message)
    else:
        await _refuse.finish('吃瓜群众一边去')


def _reset():
    global _player1, _player2, _gold, _started_time, _last_active_time
    _player1 = -1
    _player2 = -1
    _gold = 0
    _started_time = 0
    _last_active_time = 0
