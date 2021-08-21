import time

from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import GROUP, GroupMessageEvent, Message, MessageSegment
from nonebot.typing import T_State

from modules.user_info import UserInfo
from utils.log import logger
from .data_source import *
from .sentence import *

_plugin_name = '俄罗斯轮盘'
__plugin_usage__ = "装弹[金币][at](指定决斗对象，为空则所有群友都可接受决斗)"
russian_roulette = on_command('俄罗斯轮盘', aliases={'装弹', '俄罗斯转盘'}, permission=GROUP, priority=5, block=True)
_accept = on_command('接受', aliases={'接受决斗', '接受挑战'}, permission=GROUP, priority=5, block=True)
_refuse = on_command('拒绝', aliases={'拒绝决斗', '拒绝挑战'}, permission=GROUP, priority=5, block=True)
_shot = on_command('开枪', aliases={'咔', '嘭', '嘣'}, permission=GROUP, priority=5, block=True)


@russian_roulette.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    player1_id = event.sender.user_id
    # 获取最近一场决斗
    latest_duel = await get_latest_duel(group_id)
    # 若决斗有效
    if latest_duel is not None and latest_duel.active():
        logger.info(f'当前决斗: {latest_duel}')
        if latest_duel.expired():
            # 超时后终止上一个决斗
            await duel_end(latest_duel)
        # 若决斗未超时，则发送通知并跳过后续步骤
        elif latest_duel.player1_id == player1_id:
            await russian_roulette.finish('请先完成当前决斗')
            return
        else:
            await russian_roulette.finish('请勿打扰别人神圣的决斗，丨')
            return

    message = event.message
    if len(message) < 1:
        await russian_roulette.finish(f'请按照格式: {__plugin_usage__}')
        return
    # 命令后第一个参数必须为数字，作为赌注
    gold = 0
    gold_message = message[0]
    if gold_message.is_text:
        message_text = str(gold_message).strip()
        if message_text.isdigit():
            gold = int(message_text)

    if gold == 0:
        await russian_roulette.finish(f'请按照格式: {__plugin_usage__}')
        return
    elif gold < 0:
        await russian_roulette.finish('咋地，决斗完还想倒吸钱啊?')
        return

    # 获取第一个被@的人作为被挑战者
    player2_id = -1
    for item in message:
        if item.type == 'at':
            player2_id = int(item.data.get('qq', -1))
            break

    # 检测决斗发起人是否有足够的金币
    player1_gold = await UserInfo.get_gold(player1_id, group_id)
    if player1_gold < gold:
        await russian_roulette.finish(f'请出门左转打工挣够钱再来')
        return
    # 若指定了被决斗者，则检测其金币是否足够
    if player2_id != -1:
        player2_gold = await UserInfo.get_gold(player2_id, group_id)
        if player2_gold < gold:
            await russian_roulette.finish(f'你的对手太穷了，他不配和你对战')
            return

    # 若无指定被决斗者，则所有群员都可响应这场决斗
    if player2_id == -1:
        # 插入新的决斗记录
        await insert_duel(group_id, player1_id, player2_id, gold)
        await russian_roulette.finish(random_sentence(group_challenge))
    # 不能和自己决斗
    if player2_id == player1_id:
        await russian_roulette.finish(f'珍爱生命，不要自残', at_sender=True)
    # 也不允许向机器人发起决斗
    elif player2_id == event.self_id:
        await russian_roulette.finish('敢向裁判挑战? 不怕我毙了你嘛')
    else:
        # 插入新的决斗记录
        await insert_duel(group_id, player1_id, player2_id, gold)
        # 向被决斗者发送at消息
        random_s = random_sentence(challenge)
        message = Message(f'{MessageSegment.at(player2_id)}{random_s}')
        await russian_roulette.finish(message)


@_accept.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    # 获取最近一场决斗
    latest_duel = await get_latest_duel(group_id)
    # 决斗可能因超时被取消(或根本无发生过任何决斗)
    if latest_duel is None or not latest_duel.can_be_accept():
        await _accept.finish('当前无任何决斗，你接受个什么劲儿')
        return
    # 若决斗超时则跳过后续步骤(更新其状态)
    if latest_duel.expired():
        await duel_end(latest_duel)
        await _accept.finish('决斗已经超时，请重新发起')
        return
    accept_id = event.user_id
    player1_id = latest_duel.player1_id
    player2_id = latest_duel.player2_id
    # 用户是否有资格接受决斗(当前决斗未指定任何人，或接受用户是被决斗者)
    if player2_id == -1 or player2_id == accept_id:
        player2_id = accept_id
        latest_duel.player2_id = player2_id
        player2_gold = await UserInfo.get_gold(player2_id, group_id)
        if player2_gold < latest_duel.wager:
            await russian_roulette.finish(f'你的金币不足以支付决斗费用，请去打工再来')
            return
        # 进入下一阶段
        await duel_accept(latest_duel)
        random_s = random_sentence(accept_challenge)
        message = Message(f'{MessageSegment.at(player2_id)}{random_s}{MessageSegment.at(player1_id)}')
        await _accept.send(message)
        await _accept.finish('请通过[开枪]来把握自己的命运')
    else:
        await _accept.finish('和你无关，一边玩泥巴去!')


@_refuse.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    # 获取最近一场决斗
    latest_duel = await get_latest_duel(group_id)
    # 决斗可能因超时被取消(或根本无发生过任何决斗)
    if latest_duel is None or not latest_duel.can_be_accept():
        await _refuse.finish('当前无任何决斗，你怂个啥哦')
        return
    # 若决斗超时则跳过后续步骤(更新其状态)
    if latest_duel.expired():
        await duel_end(latest_duel)
        await _accept.finish('决斗已经超时了，挺起腰板吧')
        return
    refuse_id = event.user_id
    player1_id = latest_duel.player1_id
    player2_id = latest_duel.player2_id
    if player2_id == -1:
        await _refuse.finish('这场决斗面向所有人，不用站出来认怂')
        return
    if player2_id == refuse_id:
        # 更新决斗状态
        await duel_denied(latest_duel)
        message = Message(f'卑微的{MessageSegment.at(player2_id)}拒绝了应用的{MessageSegment.at(player1_id)}')
        await _refuse.finish(message)
    else:
        await _refuse.finish('吃瓜群众一边去')


@_shot.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    latest_duel = await get_latest_duel(group_id)
    if latest_duel is None or not latest_duel.in_duel():
        await _shot.finish('射射射，你射个啥呢，没有决斗!')
        return
    # 检测命令发送者id是否和当前记录的开枪人一致
    shot_player_id = event.user_id
    if shot_player_id != latest_duel.in_turn:
        await _shot.finish(f'枪不在你手上，别捣乱')
        return

