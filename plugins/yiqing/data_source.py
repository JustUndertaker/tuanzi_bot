from datetime import datetime
import httpx
import json
import os.path

from configs.pathConfig import YIQING_DATA_PATH
from utils.user_agent import get_user_agent


async def get_yiqing_data(province, city_='') -> str:
    '''
    :说明
        * 通过城市名称获取疫情数据

    :参数
        * province：省名称的简称
        * city_：城市名称

    :返回
        * str：数据
    '''
    # 获取当前时间
    today = datetime.today().strftime('%Y-%m-%d')

    # 获取文件内的时间并判断
    filename = YIQING_DATA_PATH+'yiqing.json'
    if not os.path.exists(filename):
        yiqingdict = await refresh_yiqing_data(today, filename)
    else:
        with open(filename, mode='r', encode='utf-8') as f:
            yiqingdict = json.load(f)
        filedate = yiqingdict['date']
        if today != filedate:
            yiqingdict = await refresh_yiqing_data(today, filename)
    datalist = yiqingdict['data']

    result = {}
    for data in datalist:
        if data['provinceShortName'] == province:
            if city_ == '':
                # 查询一个省的数据
                result['currentConfirmedCount'] = str(data['currentConfirmedCount'])  # 现存确诊
                result['confirmedCount'] = str(data['confirmedCount'])  # 累计确诊
                result['curedCount'] = str(data['curedCount'])  # 治愈数
                result['deadCount'] = str(data['deadCount'])  # 死亡数
                break
            else:
                # 查询城市数据
                for city in data['cities']:
                    if city['cityName'] == city_:
                        result['currentConfirmedCount'] = str(city['currentConfirmedCount'])  # 现存确诊
                        result['confirmedCount'] = str(city['confirmedCount'])  # 累计确诊
                        result['curedCount'] = str(city['curedCount'])  # 治愈数
                        result['deadCount'] = str(city['deadCount'])  # 死亡数
                        break
                break

    # 制作疫情数据图像
    # TODO：制作图像


async def refresh_yiqing_data(today: str, filename: str) -> dict:
    '''
    :说明
        * 刷新疫情数据，并保存

    :参数
        * today：今天的日期，形式如2021-08-11
        * filename：文件名称

    :返回
        * 获取的疫情数据
    '''

    url = "https://api.yimian.xyz/coro/"

    # 获取json
    async with httpx.AsyncClient(headers=get_user_agent()) as client:
        resp = await client.get(url)
        result = resp.json()

    # 构造字典
    yiqingdict = {
        'date': today,
        'data': result
    }

    # 保存文件
    with open(filename, mode='w', encodeing='utf-8') as f:
        json.dump(yiqingdict, f, ensure_ascii=False)

    return yiqingdict
