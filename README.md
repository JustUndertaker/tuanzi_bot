
![maven](https://img.shields.io/badge/python-3.9%2B-blue)
![maven](https://img.shields.io/badge/nonebot-2.0.0-yellow)
![maven](https://img.shields.io/badge/go--cqhttp-0.9.40--fix4-red)
# 团子机器人(tuanzi_bot)
****
此项目基于 Nonebot2 和 go-cqhttp 开发，使用Sqlite作为数据库的QQ群机器人。
## 部署
### 安装依赖
```
pip install -r requirements.txt
```
### 配置
#### configs/config.py
```
# 腾讯聊天API
SECRET_ID: str = ''
SECRET_KEY: str = ''

# 插件日志的debug信息是否显示在控制台
LOGGER_DEBUG: bool = True
```
腾讯聊天的API是使用[腾讯云接口](https://cloud.tencent.com/document/product/271/39416)的sercret_id和sercret_key，用于智能闲聊，如果不填将会使用[青云客接口](http://api.qingyunke.com/)。
#### 超级用户
.env.prod文件
```
SUPERUSERS=["你的QQ号"]
```

### 启动
```
python bot.py
```
### 日志
日志保存路径在：/log/，分为3个等级：ERROR，INFO，DEBUG，日志默认保存10天，以日期命名。
## 功能
### 通用插件
|   插件  |   命令   |   说明   |
| :----: | :----: | :----: |
|智能闲聊|@robot+内容/机器人昵称+内容|默认使用腾讯API，辅助青云客API|
|coser|cos/COS|让机器人返回一张随机美照|
|识图|识图|用于P站识图功能|
|~~涩图~~|色图/涩图|返回p站的二次元图|
|签到|签到|每天0点重置，会获得金币和好感度，同时有今日运气，可自行拓展|
|用户信息|我的|返回当前的金币等数据|
|天气|XX天气/天气 XX|返回XX的天气数据|
|识番|识番|通过whatanime的api以图识番|
|疫情|XX疫情/疫情 XX|返回XX地区的疫情情况|
|俄罗斯转盘|装弹\[金额\]\[at\]|群内俄罗斯轮盘小游戏|

开发新的插件可以直接放置在 plugins/ 文件夹下
### 插件管理器
>命令：菜单/功能

开放对象：所有群员，返回当前所有的插件和状态

>命令：设置 XXX 开/关

开放对象：超级用户，群管理。设置某个插件的开关状态

>命令：更新

开放对象：超级用户

手动更新某个群内的信息。


## 感谢
* [onebot](https://github.com/howmanybots/onebot)：聊天机器人应用接口标准。
* [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)：cqhttp的golang实现。
* [nonebot2](https://github.com/nonebot/nonebot2)：跨平台Python异步机器人框架。
* [zhenxun_bot](https://github.com/HibiKier/zhenxun_bot)：非常可爱的绪山真寻bot，参考了很多项目结构。
