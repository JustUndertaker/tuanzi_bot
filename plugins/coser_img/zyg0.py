import httpx

from nonebot.adapters.cqhttp import MessageSegment


# 目前已404，留作备用
def img_from_zyg0():
    r = httpx.get('https://api.zyg0.com/api/cos.php', verify=False)
    if r.status_code != 200:
        raise Exception('异常返回码')
    else:
        print(r.text.strip())
        message = MessageSegment.image(r.text.strip())
        return message
