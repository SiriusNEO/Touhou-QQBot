from not_command import *

import json
import os
import datetime

class SyncRunner:
    app: GraiaMiraiApplication
    target_group: Group
    reported: bool
    alarmed: bool

    def __init__(self, _app):
        self.app = _app
        self.reported = False

    async def async_init(self):
        self.target_group = await self.app.getGroup(WORKING_GROUP)

    async def send_text(self, text: str):
        await self.app.sendGroupMessage(self.target_group, MessageChain.create([Plain(text)]))


async def report_time(runner: SyncRunner):
    now_datetime = datetime.datetime.now()

    if now_datetime.min != 0:
        runner.reported = False
        return

    if runner.reported:
        return

    await runner.send_text("整点报时！现在是：" + str(datetime.datetime.now().hour) + "点整 ~ ")
    runner.reported = True


async def report_alarm(runner: SyncRunner):
    if os.path.exists(ALARM_PATH):
        fp = open(ALARM_PATH, "r")
        alarms = json.load(fp=fp)
        fp.close()
        now_time = time.localtime(time.time())
        alarmed_modify = True
        for alarm in alarms:
            alarm_time = time.strptime(alarm, TIME_FORMAT)
            if alarm_time.tm_hour == now_time.tm_hour and alarm_time.tm_min == now_time.tm_min:
                alarmed_modify = False
                if not runner.alarmed:
                    await runner.send_text(alarms[alarm])
                    runner.alarmed = True
                    break
        if alarmed_modify:
            runner.alarmed = False


async def run(app: GraiaMiraiApplication):
    await asyncio.sleep(START_WAIT)
    runner = SyncRunner(app)
    await runner.async_init()

    online_lock = False

    while True:
        if not online_lock:
            await runner.send_text(ONLINE + "\n" + GUIDE_DOC)
            online_lock = True

        # print("alive...")

        await asyncio.sleep(RUNNER_WAIT)
        await report_time(runner)
        await report_alarm(runner)