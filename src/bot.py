from async_runner import *
from not_command import *
from graia.application.event.mirai import BotOnlineEvent
import global_v

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)

app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://" + HOST + ":" + PORT,  # 填入 httpapi 服务运行的地址
        authKey=AUTHKEY,  # 填入 authKey
        account=ACCOUNT,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

# Init

ncrunner = NCRunner(app)

fetcher = Fetcher()

loop.create_task(run(app))

@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication,
                                  friend: Friend,
                                  message: MessageChain):
    command = command_parser(message)
    if command.typ != CommandType.ERROR:
        execute_result = await execute(command, None, fetcher)
        await app.sendGroupMessage(WORKING_GROUP, MessageChain.create(execute_result))
        if execute_result[0] == Plain(OFFLINE):
            exit(0)


@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication,
                                 group: Group,
                                 member: Member,
                                 message: MessageChain):
    
    if group.id == WORKING_GROUP:
        if global_v.bot_mode == 3 or member.id not in OTHER_BOTS:
            command = command_parser(message, global_v.bot_mode)
            #print(command.error_info)
            #print(command.typ)
            if message.has(Quote):
                quote_id = message.get(Quote)[0].origin.get(Source)[0].id
                try:
                    group_message = await app.messageFromId(quote_id)
                except:
                    pass
                else:
                    command.message.get(Quote)[0].origin = group_message.messageChain

            # Command Part
            if command.typ != CommandType.ERROR:
                execute_result = await execute(command, member, fetcher)
                print("execute: ", execute_result)
                await app.sendGroupMessage(group, MessageChain.create(execute_result))
                if execute_result[0] == Plain(OFFLINE):
                    exit(0)
                elif execute_result[0] == Plain("模式切换成功：" + MODE_NAME_NORMAL):
                    global_v.bot_mode = 0
                elif execute_result[0] == Plain("模式切换成功：" + MODE_NAME_SILENT):
                    global_v.bot_mode = 1
                elif execute_result[0] == Plain("模式切换成功：" + MODE_NAME_QUIET):
                    global_v.bot_mode = 2
                elif execute_result[0] == Plain("模式切换成功：" + MODE_NAME_CRAZY):
                    global_v.bot_mode = 3
                elif execute_result[0] == Plain("模式切换成功：" + MODE_NAME_JUDGE):
                    global_v.bot_mode = 4

            # Not Command Part
            if global_v.bot_mode != 1:
                is_run = 0
                if global_v.bot_mode == 2:
                    random.seed()
                    is_run = random.randint(1, 100)
                if is_run < 40:
                    if command.typ == CommandType.ERROR:
                        hit = await ncrunner.react(message)
                        if not hit:
                            await ncrunner.repeat(message)

app.launch_blocking()
