import random

challenge = [
    '小兔崽子，你敢接受挑战吗?',
    '你蹲坑的时候被人点名了，快提起裤子出来迎战',
    '有人叫你回家吃子弹',
    '子弹滞销了，快帮帮我们',
    '快拿起你的小手枪迎战吧',
    '虎落平阳被犬欺，来决出谁是小狗吧',
    '快端起你的黄金AK迎战吧',
    '安拉胡阿克巴!!!',
    '呜啦啦啦啦!!!',
]

group_challenge = [
    '有小兔崽子接受挑战吗',
    '有人踩场子了，快来人把他撵出去',
    '这么大群人还怕一个人吗?',
    '那么，有哪位幸运的群员要出来打枪呢?',
]

accept = [
    '掏出了他的超级大炮准备迎战',
    ', 出击! 目标: ',
    '准备要干死',
    '接受了挑战，对手是',
]

refuse = [
    '表示害怕，拒绝了',
    '怂了，不敢直面',
]

miss = [
    '呼呼，没有爆裂的声响，你活了下来',
    '虽然黑洞洞的枪口很恐怖，但好在没有子弹射出来，你活下来了',
    '\"咔\"，你没死，看来运气不错',
]

died = [
    '\"嘭！\"，你直接去世了',
    '眼前一黑，你直接穿越到了异世界...(死亡)',
    '终究还是你先走一步...',
]


def random_sentence(l) -> str:
    return l[random.randint(0, len(l) - 1)]
