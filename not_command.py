from executor import *

class NCRunner:
    app: GraiaMiraiApplication
    target_group: Group

    repeat_cache: MessageChain
    repeat_counter: int

    def __init__(self, _app):
        self.app = _app
        self.reported = False
        self.repeat_counter = 0

    async def async_init(self):
        self.target_group = await self.app.getGroup(WORKING_GROUP)

    async def send_text(self, text: str):
        await self.app.sendGroupMessage(self.target_group, MessageChain.create([Plain(text)]))

    async def save_image(self, url: str):
        fp = open(IMG_PATH + "tmp.jpg", "wb")
        data = await Image.http_to_bytes(Image(), url)
        fp.write(data)

    async def download_image(self, url: str):
        return await Image.http_to_bytes(Image(), url)

    async def comment(self, message: MessageChain):
        await self.async_init()
        if os.path.exists(COMMENT_PATH):
            fp = open(COMMENT_PATH, "r")
            comments = json.load(fp=fp)
            fp.close()
            if not message.has(Plain):
                return
            text_str = message.get(Plain)[0].asDisplay()
            for comment in comments:
                if comments[comment][1] and comment == text_str:
                    await self.send_text(comments[comment][0])
                    break

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
            message_pic = await self.download_image(message.get(Image)[0].url)
            sender.append(message.get(Image)[0])
        else:
            message_pic = ""
        if self.repeat_counter > 0 and len(self.repeat_cache.get(Plain)) > 0:
            cache_text = self.repeat_cache.get(Plain)[0].asDisplay()
        else:
            cache_text = ""
        if self.repeat_counter > 0 and len(self.repeat_cache.get(Image)) > 0:
            cache_pic = await self.download_image(self.repeat_cache.get(Image)[0].url)
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

        print(self.repeat_counter, self.repeat_cache)

        if self.repeat_counter >= REPEAT_LEN:
            await self.app.sendGroupMessage(self.target_group, MessageChain.create(sender))
            self.repeat_counter = 0

