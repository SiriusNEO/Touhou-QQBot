from executor import *
import datetime
import global_v

judge_commment = [
    "几把", "不太行", "一般般", "小行", "彳亍", "好好好好好", "行中行之大行特行",
    "社了", "傻逼", "乐", "好大", "该冲了", "k48", "?", "出货了", "不评价", "臭寄吧",
    "鬼！", "小好", "你是傻逼？", "草", "爹", "癌症晚期", "ybb", "好活", "滑了",
    "就那样", "普通", "你爹", "不够色", "色", "再来点", "急了", "有点烂", "有点好",
    "超市", "🥵", "🤤", "🥵🥵🥵", "😅", "狗头", "suki", "你再发？", "寄", "我不好说",
    "郭楠", "大便", "勾八", "cfy", "东方project", "福州一中", "alksdjflskjfs", "%$^&*^*&^?>",
    "古神", "不可名状", ""
]

class NCRunner:
    app: GraiaMiraiApplication
    target_group: Group

    repeat_cache: MessageChain
    repeat_counter: int

    last_react_time: datetime.datetime

    def __init__(self, _app):
        self.app = _app
        self.reported = False
        self.repeat_counter = 0
        self.last_react_time = datetime.datetime.now()

    async def async_init(self):
        self.target_group = await self.app.getGroup(WORKING_GROUP)

    async def send_text(self, text: str):
        await self.app.sendGroupMessage(self.target_group, MessageChain.create([Plain(text)]))

    async def reply_text(self, text: str, message: MessageChain):
        await self.app.sendGroupMessage(self.target_group, MessageChain.create([Plain(text)]), 
                                        quote = message.get(Source)[0])    

    async def send_local_image(self, path: str):
        await self.app.sendGroupMessage(self.target_group, MessageChain.create([Image.fromLocalFile(path)]))

    async def react(self, message: MessageChain,):
        await self.async_init()
        hit = False

        now_datetime = datetime.datetime.now()
        delta = now_datetime.__sub__(self.last_react_time)
        if global_v.bot_mode != 3 and delta.seconds <= 15:  # 15s 冷静期
            return hit

        # judge img
        if global_v.bot_mode == 4 and message.has(Image):
            time.sleep(RANDOM_WAIT)
            random.seed()
            judge = random.randint(0, len(judge_commment))
            time.sleep(THINK_WAIT)
            await self.reply_text("评价为" + judge_commment[judge], message) 

        # react img
        if os.path.exists(IMG_MAP_PATH):
            fp = open(IMG_MAP_PATH, "r")
            img_map = json.load(fp)
            fp.close()
            if not message.has(Plain):
                return False
            text_str = message.get(Plain)[0].asDisplay()
            text_str = text_str.replace(BLANK_REPLACE, " ")
            for img in img_map:
                if img_map[img][1] == 2 and text_str.find(img) != -1:
                    await self.send_local_image(img_map[img][0])
                    hit = True
                    break
                elif img_map[img][1] == 1 and img == text_str:
                    await self.send_local_image(img_map[img][0])
                    hit = True
                    break

        # react comment
        if os.path.exists(COMMENT_PATH):
            fp = open(COMMENT_PATH, "r")
            comments = json.load(fp=fp)
            fp.close()
            if not message.has(Plain):
                return False
            text_str = message.get(Plain)[0].asDisplay()
            text_str = text_str.replace(BLANK_REPLACE, " ")
            for comment in comments:
                if comments[comment][1] == 2 and text_str.find(comment) != -1:
                    await self.send_text(comments[comment][0])
                    hit = True
                    break
                elif comments[comment][1] == 1 and comment == text_str:
                    await self.send_text(comments[comment][0])
                    hit = True
                    break

        if hit:
            self.last_react_time = datetime.datetime.now()

        return hit

    async def repeat(self, message: MessageChain):
        await self.async_init()

        sender = list()

        if message is None or (not message.has(Plain) and not message.has(Image)):
            self.repeat_counter = 0
            return
        if len(message.get(Plain)) > 0:
            message_text = message.get(Plain)[0].asDisplay()
            sender.append(message.get(Plain)[0])
        else:
            message_text = ""
        if len(message.get(Image)) > 0:
            message_pic = await download_image(message.get(Image)[0].url)
            sender.append(message.get(Image)[0])
        else:
            message_pic = ""
        if self.repeat_counter > 0 and len(self.repeat_cache.get(Plain)) > 0:
            cache_text = self.repeat_cache.get(Plain)[0].asDisplay()
        else:
            cache_text = ""
        if self.repeat_counter > 0 and len(self.repeat_cache.get(Image)) > 0:
            cache_pic = await download_image(self.repeat_cache.get(Image)[0].url)
        else:
            cache_pic = ""

        # 复读
        if self.repeat_counter == 0:
            self.repeat_cache = message
            self.repeat_counter = 1

        elif message_text == cache_text and message_pic == cache_pic:
            self.repeat_counter += 1
        else:
            self.repeat_counter = 0

        # print(self.repeat_counter, self.repeat_cache)

        if self.repeat_counter == REPEAT_LEN:
            await self.app.sendGroupMessage(self.target_group, MessageChain.create(sender))

