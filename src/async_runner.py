from not_command import *

import json
import os
import datetime
import global_v

class AsyncRunner:
    app: GraiaMiraiApplication
    target_group: Group
    next_time: int

    def __init__(self, _app):
        self.app = _app
        self.reported = False
        random.seed()
        self.next_time = random.randint(1, 59)

    async def async_init(self):
        self.target_group = await self.app.getGroup(WORKING_GROUP)

    async def send_text(self, text: str):
        await self.app.sendGroupMessage(self.target_group, MessageChain.create([Plain(text)]))

    async def send_local_image(self, path: str):
        await self.app.sendGroupMessage(self.target_group, MessageChain.create([Image.fromLocalFile(path)]))


async def report_time(runner: AsyncRunner, now_datetime):
    now_datetime = datetime.datetime.now()
    if now_datetime.minute != 0 or now_datetime.second != 0 or (3 <= now_datetime.hour <= 6):
        return

    text_str = "整点报时！现在是：" + str(datetime.datetime.now().hour) + "点整~"

    if now_datetime.hour == 2:
        # 晚安
        text_str += "\n" + GOOD_NIGHT

    if now_datetime.hour == 7:
        # 早安
        text_str += "\n" + GOOD_MORNING + str(now_datetime.month) + "月" + str(now_datetime.day) + "号，" + weekdayName[now_datetime.weekday()] + "~"

    await runner.send_text(text_str)
    random.seed()
    runner.next_time = random.randint(1, 59)


async def report_alarm(runner: AsyncRunner, now_datetime):
    if os.path.exists(ALARM_PATH):
        fp = open(ALARM_PATH, "r")
        alarms = json.load(fp=fp)
        fp.close()
        now_time = time.localtime(time.time())
        for alarm in alarms:
            alarm_time = time.strptime(alarm, TIME_FORMAT)
            if alarm_time.tm_hour == now_time.tm_hour and alarm_time.tm_min == now_time.tm_min and now_time.tm_sec == 0:
                await runner.send_text(alarms[alarm])
                break


async def spontaneous_image(runner: AsyncRunner, now_datetime):
    random.seed()

    now_datetime = datetime.datetime.now()

    if global_v.bot_mode != 3:
        if (3 <= now_datetime.hour <= 6) or now_datetime.hour % 2 == 0:  # 奇数小时发送
            return

        if now_datetime.minute != runner.next_time:
            return
    else:
        if now_datetime.minute % 2 == 0: # 奇数分钟
            return

    if now_datetime.second != 0:
        return

    if os.path.exists(IMG_MAP_PATH):
        fp = open(IMG_MAP_PATH, "r")
        img_map = json.load(fp)
        fp.close()

        img_map_list = list(img_map)
        index = random.randint(1, len(img_map_list))
        await runner.send_local_image(img_map[img_map_list[index-1]][0])


async def spontaneous_cm(runner: AsyncRunner, now_datetime):
    random.seed()

    if global_v.bot_mode != 3:
        if (3 <= now_datetime.hour <= 6) or now_datetime.hour % 2 == 1:  # 偶数小时发送
            return

        if now_datetime.minute != runner.next_time:
            return
    else:
        if now_datetime.minute % 2 == 1:  # 偶数分钟
            return
        
    if now_datetime.second != 0:
        return

    if os.path.exists(COMMENT_PATH):
        fp = open(COMMENT_PATH, "r")
        comments = json.load(fp)
        fp.close()

        comments_list = list(comments)
        index = random.randint(1, len(comments_list))
        await runner.send_text(comments[comments_list[index-1]][0])


async def run(app: GraiaMiraiApplication):
    await asyncio.sleep(START_WAIT)
    runner = AsyncRunner(app)
    await runner.async_init()

    online_lock = False

    while True:
        if not online_lock:
            await runner.send_text(ONLINE + "\n" + GUIDE_DOC)
            online_lock = True
        # print("alive...")
        await asyncio.sleep(RUNNER_WAIT)
        now_datetime = datetime.datetime.now()
        if global_v.bot_mode != 1:
            await spontaneous_image(runner, now_datetime)
            await spontaneous_cm(runner, now_datetime)
            await report_time(runner, now_datetime)
            await report_alarm(runner, now_datetime)