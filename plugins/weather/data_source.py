import httpx
from PIL import Image, ImageDraw, ImageFont, ImageOps
from nonebot import message
from configs.pathConfig import PATH_PLUGIN_WEATHER
from config import WEATHER_INFO, WIND_INFO, OTHER_INFO


async def get_weather_of_city(city) -> message:
    '''
    通过城市名称获取天气结果
    :city：城市名
    :返回：message消息内容
    '''
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + city
    try:
        data_json = httpx.get(url).json()
        if data_json['desc'] != "OK":
            result = "查询失败！"
            return result
        return data_json['data']['forecast'][0]['type']
    except:
        result = "查询失败！"
        return result

def _get_date_info(date_str) -> str:
    '''
    通过字典给定的date，获取具体星期几
    :返回：昨天，今天，星期一...星期天
    '''

async def _create_little_card(data) -> Image:
    '''
    创建日期小卡片
    :data 天气数据
    :返回：Image类
    '''


async def _draw_card_of_weather(data) -> str:
    '''
    根据返回的data画出天气卡片
    '''
