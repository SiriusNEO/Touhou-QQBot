# Touhou-QQBot (Mirai & Graia Framework)

<div align="center">
	<img src="assets/avatar.jpg" width="300px">
</div>

### 简介

自用的 qq 群娱乐机器人，适用于东方 Project 相关群聊。

目前版本：![python3](https://img.shields.io/badge/version-0.9-red)

稳定运行的 Python 版本  ![python3](https://img.shields.io/badge/python-3.8.5-blue)  

稳定运行的服务器的操作系统  ![](https://img.shields.io/badge/CentOS-7-yellow)

感谢以下开源项目给本项目给予的诸多帮助：

- [mirai](https://github.com/mamoe/mirai) 高效率 QQ 机器人支持库
- [GraiaApplication](https://github.com/GraiaProject/Application)  基于 mirai-api-http 的 Python 框架

**警告：由于腾讯的风控，该机器人并不稳定，很可能会发生局部功能失效、版本落后等情况，请谨慎食用！**



### 部署与使用

**环境**

配置 [mirai](https://github.com/mamoe/mirai) 以及 [mirai-api-http](https://github.com/project-mirai/mirai-api-http)

配置 [GraiaApplication][https://github.com/GraiaProject/Application] ，确保在你的虚拟环境下能正常运行 Graia 文档中的 demo 机器人

配置 Python venv（可以使用 `requirements.txt`）

```
graia-application-mirai 0.18.4
graia-broadcast         0.8.11
Pillow                  8.3.1
pydantic                1.7.1
numpy                   1.21.2
requests                2.26.0
beautifulsoup4          4.9.3
selenium                2.48.0
```

请在 `constant.py`  中**将环境变量修改为你自己的参数！！！**

一些比较重要的参数：

```python
# 主机地址
# 如果你的mirai和bot.py部署在同一台设备上，请务必使用localhost
HOST =  

# 端口号
# 请注意防火墙问题
PORT = 

# 与 setting.yml 保持一致
AUTHKEY = 

# 你的bot qq 号
ACCOUNT = 

# bot 名字 只用于显示
BOT_NAME = "RobustBotQQ"

# 管理员qq账号, 目前没有完整的权限系统, 用途仅仅是对该用户开放退出命令
ROOT = 

# 其它Bot qq号的表单
# 一个群聊中如果有多个机器人, 容易产生相互调用死循环问题, 填入此表单可以屏蔽它们
# mod 为狂野模式时会与其它机器人互动
OTHER_BOTS = []
```

要改变说明文字，请修改 `illustration.py`  

由于爬虫的需要，还需要下载 `ChromeDriver` ，并在 `asoul.py` 中修改你的 driver 路径

**使用**

- 打开 mcl，确保终端能接收到 qq 群信息

- `python3 bot.py` 运行，在群聊中弹出开机提示语说明运行成功



### 需求

- [x] 帮助
- [x] 随机数：测人品，冲不冲，麦不麦
- [x] 抽东方人物
- [x] 自动复读
- [x] 评论
- [x] ~~小作文发病~~ asoul 模块暂不可用
- [x] 非命令格式的怪话回复
- [x] 整点报时、闹钟
- [x] 图片点评



### 设计

**命令格式**

```
。<command-name> <args1> <args2> ...
```

详细使用方法请启动机器人并使用它的帮助功能 `。h` 查看，本文档不赘述。



### 其它

- QQ 聊天机器人为官方所不鼓励，请谨慎使用，尽量使用小号测试。

- 本 Bot 由于主要目的是自用，因此其中含有大量个人兴趣爱好相关的功能与要素（包括东方人物抽取、ASoul 小作文爬虫发送等等），不喜勿用。