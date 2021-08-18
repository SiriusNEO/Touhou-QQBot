from sync_runner import *
from not_command import *

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)

app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:20001",  # 填入 httpapi 服务运行的地址
        authKey="miraikey",  # 填入 authKey
        account=1378438181,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

ncrunner = NCRunner(app)

loop.create_task(run(app))

@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication,
                                  friend: Friend,
                                  message: MessageChain):
    command = command_parser(message)
    print(command.error_info)
    print(command.args)

    if message.hasText("call rbq"):
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain("Hello, World!")
        ]))

@bcc.receiver("GroupMessage")
async def group_message_listener(app: GraiaMiraiApplication,
                                 group: Group,
                                 member: Member,
                                 message: MessageChain):

    if group.id == WORKING_GROUP:
        command = command_parser(message)
        print(command.error_info)
        print(command.args)

        # Command Part
        if command.typ != CommandType.ERROR:
            execute_result = execute(command, member)
            await app.sendGroupMessage(group, MessageChain.create(execute_result))
            if execute_result[0] == Plain(OFFLINE):
                exit(0)

        # Not Command Part
        await ncrunner.comment(message)
        command = command_parser(message)
        if command.typ == CommandType.ERROR:
            await ncrunner.repeat(message)

app.launch_blocking()
