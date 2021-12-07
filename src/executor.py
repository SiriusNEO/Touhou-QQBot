from command import *
from illustration import *
from graia.application import *
from graia.application.group import Group, Member
from graia.application.message.elements.internal import Plain, Image, At, Quote
from PIL import Image as PIL_IM
from asoul import *
from touhou import *
import random
import time
import os
import json


def rp_level(lucky: int):
    if lucky < 5:
        return "大凶"
    elif lucky < 15:
        return "凶"
    elif lucky < 30:
        return "末吉"
    elif lucky < 45:
        return "吉"
    elif lucky < 60:
        return "小吉"
    elif lucky < 70:
        return "中吉"
    return "大吉"


def random_str(slen = 32):
    random.seed()
    ret = ''
    base = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    base_len = len(base) - 1
    for i in range(slen):
        ret += base[random.randint(0, base_len)]
    return ret


async def save_image(url: str, file_name="tmp"):
    fp = open(IMG_PATH + file_name, "wb")
    data = await Image.http_to_bytes(Image(), url)
    fp.write(data)


async def download_image(url: str):
    return await Image.http_to_bytes(Image(), url)


async def execute(command: Command, commander: Member, fetcher: Fetcher):
    """
    执行命令

    :param command: Command
    :param commander: 执行者
    :returns: list, 初始化 MessageChain
    """
    sender = list()
    text_str = str()
    img_path_str = str()
    img_send_mode = str()
    at_id = 0
    if command.typ == CommandType.HELP:
        if len(command.args) == 0:
            text_str = GUIDE_DOC
        elif len(command.args) == 1:
            if command.args[0] == HELP_ARG_INS:
                text_str = INS_DOC
            elif command.args[0] == HELP_ARG_DETAIL:
                text_str = DETAIL_DOC
            elif command.args[0] == HELP_ARG_MORE:
                text_str = MORE_DOC
            elif command.args[0] == HELP_ARG_HINT:
                text_str = HINT_DOC
            elif command.args[0] == HELP_INS:
                text_str = HELP_DOC
            elif command.args[0] == RANDOM_INS:
                text_str = RANDOM_DOC
            elif command.args[0] == COMMENT_INS:
                text_str = COMMENT_DOC
            elif command.args[0] == ALARM_INS:
                text_str = ALARM_DOC
            elif command.args[0] == ASOUL_INS:
                text_str = ASOUL_DOC
            elif command.args[0] == TOUHOU_INS:
                text_str = TOUHOU_DOC
            elif command.args[0] == IMG_INS:
                text_str = IMG_DOC
            elif command.args[0] == MODE_INS:
                text_str = MODE_DOC
            elif command.args[0] == EXIT_INS:
                text_str = EXIT_DOC
            else:
                text_str = ARG_ERROR
        else:
            text_str = ARG_ERROR

    elif command.typ == CommandType.RANDOM:
        if command.times <= 0 or command.times > TIMES_LIMIT:
            text_str = TIMES_ERROR
        else:
            for tim in range(command.times):
                time.sleep(RANDOM_WAIT)
                random.seed()
                if tim >= 1:
                    text_str += "\n"
                if len(command.args) == 0:
                    command.args.append("100")
                if len(command.args) == 1:
                    if command.args[0].isdigit():
                        ranger = int(command.args[0])
                        if ranger <= 0:
                            text_str = ARG_ERROR
                        else:
                            result = random.randint(1, ranger)
                            if commander is not None:
                                at_id = commander.id
                            text_str += RANDOM_RESULT + "D" + str(ranger) + "=" + str(result)

                    elif len(command.args[0]) == 1:
                        todo = (random.randint(0, 1) == 1)
                        if commander is not None:
                            at_id = commander.id
                        if todo:
                            text_str += str(command.args[0] + "!")
                        else:
                            text_str += str("不" + command.args[0] + "，算了吧...")

                    elif command.args[0] == RANDOM_ARG_WORD:
                        fp = open(WORD_PATH, "r")
                        word = json.load(fp)
                        random.seed()
                        word_list = list(word)
                        index = random.randint(1, len(word_list))
                        if commander is not None:
                            at_id = commander.id
                        text_str += word_list[index-1]

                    elif command.args[0] == RANDOM_ARG_GK:
                        chinese = int(random.gauss(120, 5))
                        math = int(random.gauss(125, 15))
                        english = int(random.gauss(137, 6))
                        if chinese > 145:
                            chinese = 145
                        if math > 149:
                            math = 150
                        if english > 149:
                            english = 149
                        text_str += "您参加普通高等学校招生全国统一考试的分数是：" + \
                                   "\n语文：" + TAB + str(chinese) + "/150" \
                                                                  "\n数学：" + TAB + str(math) + "/150" \
                                                                                              "\n英语：" + TAB + str(
                            english) + "/150"

                        zonghe = int(random.gauss(250, 25))
                        if zonghe > 299:
                            zonghe = 299
                        text_str += "\n理综：" + TAB + str(zonghe) + "/300"
                        text_str += "\n总分：" + TAB + str(chinese + math + english + zonghe) + "/750"
                        if commander is not None:
                            at_id = commander.id

                    elif command.args[0] == RANDOM_ARG_RP:
                        lucky = random.randint(1, 100)

                        text_str += "您的今日运势是：" + str(lucky) + "，" + rp_level(lucky)
                        if commander is not None:
                            at_id = commander.id

                        fp = open(RP_PATH, "r")
                        rp_list = list(json.load(fp))

                        good_behavior = random.randint(1, len(rp_list))
                        bad_behavior = random.randint(1, len(rp_list))

                        text_str += "\n宜：" + rp_list[good_behavior - 1]
                        text_str += "\n忌：" + rp_list[bad_behavior - 1]

                    else:
                        text_str = ARG_ERROR

                elif len(command.args) == 2:
                    if command.args[0] == RANDOM_ARG_RP:
                        if command.times > 1:
                            text_str = TIMES_ERROR
                        else:
                            fp = open(RP_PATH, "r")
                            rp_dict = json.load(fp=fp)
                            if command.args[1] == ARG_LS:
                                rp_list = list(rp_dict)
                                text_str += "当前运势词库："
                                if len(rp_list) > OVERFLOW_LEN:
                                    rp_list = rp_list[len(rp_list)-OVERFLOW_LEN:len(rp_list)]
                                    text_str += "..."
                                for i in range(len(rp_list)):
                                    if i != 0:
                                        text_str += "，"
                                    text_str += rp_list[i]
                            else:
                                command.args[1] = command.args[1].replace(BLANK_REPLACE, " ")
                                rp_dict[command.args[1]] = True
                                fp.close()
                                fp = open(RP_PATH, "w")
                                json.dump(rp_dict, fp)
                                text_str += "RP词条添加成功！"

                    elif command.args[0].isdigit() and command.args[1].isdigit():
                        ranger = int(command.args[0])
                        checker = int(command.args[1])
                        if ranger <= 0:
                            text_str = ARG_ERROR
                        else:
                            result = random.randint(1, ranger)
                            text_str += RANDOM_RESULT + "D" + str(ranger) + "=" + str(result) + "，"
                            if commander is not None:
                                at_id = commander.id
                            if result > checker:
                                text_str += str(result) + ">" + str(checker) + "，检定失败..."
                            else:
                                text_str += str(result) + "<=" + str(checker) + "，检定成功!"
                    elif command.args[0] == RANDOM_ARG_GK:
                        chinese = int(random.gauss(120, 5))
                        math = int(random.gauss(125, 15))
                        english = int(random.gauss(137, 6))
                        if chinese > 145:
                            chinese = 145
                        if math > 149:
                            math = 150
                        if english > 149:
                            english = 149
                        text_str += "您参加普通高等学校招生全国统一考试的分数是：" + \
                                   "\n语文：" + TAB + str(chinese) + "/150" + \
                                   "\n数学：" + TAB + str(math) + "/150" \
                                                               "\n英语：" + TAB + str(english) + "/150"

                        if command.args[1] == "文":
                            zonghe = int(random.gauss(220, 20))
                            text_str += "\n文综：" + TAB + str(zonghe) + "/300"
                        else:
                            zonghe = int(random.gauss(250, 25))
                            text_str += "\n理综：" + TAB + str(zonghe) + "/300"
                        if zonghe > 299:
                            zonghe = 299
                        text_str += "\n总分：" + TAB + str(chinese + math + english + zonghe) + "/750"
                        if commander is not None:
                            at_id = commander.id
                elif len(command.args) == 3 and command.args[0] == RANDOM_ARG_RP:
                    if command.args[1] == DEL_ARG:
                        if command.times > 1:
                            text_str = TIMES_ERROR
                        else:
                            fp = open(RP_PATH, "r")
                            rp_dict = json.load(fp=fp)
                            command.args[2] = command.args[2].replace(BLANK_REPLACE, " ")
                            if command.args[2] not in rp_dict:
                                text_str = NOT_FOUND_ERROR
                            else:
                                rp_dict.pop(command.args[2])
                                fp.close()
                                fp = open(RP_PATH, "w")
                                json.dump(rp_dict, fp)
                                text_str += "RP词条删除成功！"
                    else:
                        text_str = ARG_ERROR

                else:
                    text_str = ARG_ERROR

    elif command.typ == CommandType.COMMENT:
        if os.path.exists(COMMENT_PATH):
            fp = open(COMMENT_PATH, "r")
            comments = json.load(fp=fp)
            fp.close()
        else:
            comments = dict()
        if len(command.args) == 0:
            text_str += "当前可以评论："
            comments_list = list(comments)
            if len(comments_list) > OVERFLOW_LEN:
                text_str += "..."
                comments_list = comments_list[len(comments_list)-OVERFLOW_LEN:len(comments_list)]
            for i in range(len(comments_list)):
                if i != 0:
                    text_str += "，"
                text_str += comments_list[i]
                if comments[comments_list[i]][1] == 1:
                    text_str += "*"
                elif comments[comments_list[i]][1] == 2:
                    text_str += "^"
        elif len(command.args) == 1:
            command.args[0] = command.args[0].replace(BLANK_REPLACE, " ")
            if command.args[0] in comments:
                text_str += comments[command.args[0]][0]
            elif command.args[0].find(RANDOM_INS) == 0:
                command.times = random_parser(command.args[0])
                if command.times <= 0 or command.times > TIMES_LIMIT:
                    text_str = TIMES_ERROR
                else:
                    for tim in range(command.times):
                        time.sleep(RANDOM_WAIT)
                        random.seed()
                        if tim >= 1:
                            text_str += "\n"
                        comments_list = list(comments)
                        index = random.randint(1, len(comments_list))
                        text_str += comments[comments_list[index-1]][0]
            else:
                text_str += COMMENT_ERROR
        elif len(command.args) == 2:
            if command.args[0] == DEL_ARG:
                command.args[1] = command.args[1].replace(BLANK_REPLACE, " ")
                if command.args[1] not in comments:
                    text_str = NOT_FOUND_ERROR
                else:
                    comments.pop(command.args[1])
                    fp = open(COMMENT_PATH, "w")
                    json.dump(comments, fp)
                    fp.close()
                    text_str += "评论删除成功！"
            else:
                command.args[0] = command.args[0].replace(BLANK_REPLACE, " ")
                command.args[1] = command.args[1].replace(BLANK_REPLACE, " ")
                comments[command.args[0]] = (command.args[1], False)
                fp = open(COMMENT_PATH, "w")

                json.dump(comments, fp)
                fp.close()
                text_str += "评论添加成功！"
        elif len(command.args) == 3:
            command.args[0] = command.args[0].replace(BLANK_REPLACE, " ")
            command.args[1] = command.args[1].replace(BLANK_REPLACE, " ")
            if command.args[2] == ARG_KEY:
                comments[command.args[0]] = (command.args[1], 2)
            elif command.args[2] == ARG_AUTO:
                comments[command.args[0]] = (command.args[1], 1)
            else:
                comments[command.args[0]] = (command.args[1], 0)
            fp = open(COMMENT_PATH, "w")
            json.dump(comments, fp)
            fp.close()
            text_str += "评论添加成功！"
        else:
            text_str = ARG_ERROR

    elif command.typ == CommandType.ALARM:
        if os.path.exists(ALARM_PATH):
            fp = open(ALARM_PATH, "r")
            alarms = json.load(fp=fp)
            fp.close()
        else:
            alarms = dict()
        if len(command.args) == 0:
            text_str += "当前闹钟："
            for alarm in alarms:
                if len(alarms[alarm]) > 5:
                    text_str += "\n" + alarm + TAB + alarms[alarm][:5] + "..."
                else:
                    text_str += "\n" + alarm + TAB + alarms[alarm]
        elif len(command.args) == 2:
            if command.args[0] == DEL_ARG:
                if command.args[1] not in alarms:
                    text_str = NOT_FOUND_ERROR
                else:
                    alarms.pop(command.args[1])
                    fp = open(ALARM_PATH, "w")
                    json.dump(alarms, fp)
                    fp.close()
                    text_str += "闹钟删除成功！"
            else:
                try:
                    alarm_time = time.strptime(command.args[0], TIME_FORMAT)
                except:
                    text_str = DONT_MATCH_ERROR
                else:
                    command.args[1] = command.args[1].replace(BLANK_REPLACE, " ")
                    alarms[command.args[0]] = command.args[1]
                    text_str = "闹钟添加成功！"
                    fp = open(ALARM_PATH, "w")
                    json.dump(alarms, fp)
                    fp.close()
        else:
            text_str = ARG_ERROR

    elif command.typ == CommandType.ASOUL:
        if len(command.args) == 0:
            if commander is not None:
                at_id = commander.id
            text_str = fetcher.random_writing()
        elif len(command.args) == 1:
            if command.args[0] == ASOUL_ARG_CNKI:
                if not command.message.has(Quote):
                    text_str = CNKI_ERROR
                else:
                    quote_message = command.message.get(Quote)[0].origin
                    if not quote_message.has(Plain):
                        text_str = CNKI_ERROR
                    else:
                        origin_text = quote_message.get(Plain)[0].asDisplay()
                        if len(origin_text) < 10 or len(origin_text) > 1000:
                            text_str = CNKI_ERROR
                        else:
                            info_dict = fetcher.check_duplicate(origin_text)
                            text_str = "枝网查重报告 车车群特供版"
                            if "author" not in info_dict:
                                text_str += "\n查重率: 0%，支持原创捏"
                            else:
                                text_str += "\n" + info_dict['rate'] + \
                                            "\n" + info_dict['author'] + \
                                            "\n" + info_dict['time'] + \
                                            "\n" + info_dict['link']
            else:
                if commander is not None:
                    at_id = commander.id

                founded = False
                while not founded:
                    text_str = fetcher.random_writing()
                    for asoul in ASOUL:
                        if not founded and text_str.find(asoul) != -1:
                            founded = True
                        text_str = text_str.replace(asoul, command.args[0])

        else:
            text_str = ARG_ERROR

    elif command.typ == CommandType.TOUHOU:
        if len(command.args) == 2:
            if command.args[1] == ARG_LS:
                text_str = TOO_MUCH_ERROR
            elif command.args[1].find(RANDOM_INS) != -1:
                command.times = random_parser(command.args[1])
                if command.times <= 0 or command.times > TIMES_LIMIT:
                    text_str = TIMES_ERROR
                else:
                    for tim in range(command.times):
                        time.sleep(RANDOM_WAIT)
                        random.seed()
                        if tim >= 1:
                            text_str += "\n"
                        if command.args[0] == TOUHOU_ARG_ROLE:
                            result = get_role("")
                            if commander is not None:
                                at_id = commander.id
                            text_str += "[Touhou Role] 您抽到了："
                            text_str += "\n" + result[0]
                            text_str += "\n来自：" + result[1]
                        elif command.args[0] == TOUHOU_ARG_SC:
                            result = get_sc("")
                            if commander is not None:
                                at_id = commander.id
                            text_str += "[Touhou Spellcard] 您抽到了："
                            text_str += "\n" + result[0]
                            text_str += "\n使用者：" + result[1]
                        else:
                            text_str = ARG_ERROR
            else:
                text_str = ARG_ERROR
        elif len(command.args) == 3:
            if command.args[1] == ARG_LS:
                if command.args[0] == TOUHOU_ARG_ROLE:
                    role_list = list_role(command.args[2])
                    if len(role_list) == 0:
                        text_str = NOT_FOUND_ERROR
                    else:
                        if commander is not None:
                            at_id = commander.id
                        text_str = "[Touhou Role] 作品 [" + command.args[2] + "]："
                        for role in role_list:
                            text_str += "\n" + role
                elif command.args[0] == TOUHOU_ARG_SC:      
                    sc_list = list_sc(command.args[2])
                    if len(sc_list) == 0:
                        text_str = NOT_FOUND_ERROR
                    else:
                        if commander is not None:
                            at_id = commander.id
                        text_str = "[Touhou Spellcard] 角色 [" + command.args[2] + "]："
                        for sc in sc_list:
                            text_str += "\n" + sc
                else:
                    text_str = ARG_ERROR    
            elif command.args[1].find(RANDOM_INS) != -1:
                command.times = random_parser(command.args[1])
                if command.times <= 0 or command.times > TIMES_LIMIT:
                    text_str = TIMES_ERROR
                else:
                    for tim in range(command.times):
                        time.sleep(RANDOM_WAIT)
                        random.seed()
                        if tim >= 1:
                            text_str += "\n"
                        if command.args[0] == TOUHOU_ARG_ROLE:
                            result = get_role(command.args[2])
                            if result[0] == "":
                                text_str = NOT_FOUND_ERROR
                            else:
                                if commander is not None:
                                    at_id = commander.id
                                text_str += "[Touhou Role] 您抽到了："
                                text_str += "\n" + result[0]
                                text_str += "\n来自：" + result[1]
                        elif command.args[0] == TOUHOU_ARG_SC:
                            result = get_sc(command.args[2])
                            if result[0] == "":
                                text_str = NOT_FOUND_ERROR
                            else:
                                if commander is not None:
                                    at_id = commander.id
                                text_str += "[Touhou Spellcard] 您抽到了："
                                text_str += "\n" + result[0]
                                text_str += "\n使用者：" + result[1]
                        else:
                            text_str = ARG_ERROR
            else:
                text_str = ARG_ERROR
        else:
            text_str = ARG_ERROR
    elif command.typ == CommandType.IMG:
        if os.path.exists(IMG_MAP_PATH):
            fp = open(IMG_MAP_PATH, "r")
            img_map = json.load(fp=fp)
            fp.close()
        else:
            img_map = dict()
        if len(command.args) == 0:
            text_str += "当前可以查看："
            img_map_list = list(img_map)
            if len(img_map_list) > OVERFLOW_LEN:
                text_str += "..."
                img_map_list = img_map_list[len(img_map_list) - OVERFLOW_LEN:len(img_map_list)]
            for i in range(len(img_map_list)):
                if i != 0:
                    text_str += "，"
                text_str += img_map_list[i]
                if img_map[img_map_list[i]][1] == 1:
                    text_str += "*"
                elif img_map[img_map_list[i]][1] == 2:
                    text_str += "^"
        elif len(command.args) == 1:
            if command.message.has(Quote):
                quote_message = command.message.get(Quote)[0].origin
                if not quote_message.has(Image):
                    text_str += IMG_ERROR
                else:    
                    image = quote_message.get(Image)[0]
                    file_name = random_str()
                    await save_image(image.url, file_name)
                    command.args[0] = command.args[0].replace(BLANK_REPLACE, " ")
                    img_map[command.args[0]] = (IMG_PATH + file_name, False)
                    fp = open(IMG_MAP_PATH, "w")
                    json.dump(img_map, fp)
                    fp.close()
                    text_str += "图片添加成功！"
            else:
                command.args[0] = command.args[0].replace(BLANK_REPLACE, " ")
                if command.args[0] in img_map:
                    img_path_str += img_map[command.args[0]][0]
                elif command.args[0].find(RANDOM_INS) == 0:
                    command.times = random_parser(command.args[0])
                    if command.times <= 0 or command.times > TIMES_LIMIT:
                        text_str = TIMES_ERROR
                    else:
                        for tim in range(command.times):
                            time.sleep(RANDOM_WAIT)
                            random.seed()
                            if tim >= 1:
                                text_str += "\n"
                                img_path_str += "\n"
                            img_map_list = list(img_map)
                            index = random.randint(1, len(img_map_list))
                            img_path_str += img_map[img_map_list[index - 1]][0]
                else:
                    text_str += NOT_FOUND_ERROR
        elif len(command.args) == 2:
            command.args[1] = command.args[1].replace(BLANK_REPLACE, " ")
            if command.args[0] == DEL_ARG:
                if command.args[1] not in img_map:
                    text_str = NOT_FOUND_ERROR
                else:
                    img_map.pop(command.args[1])
                    fp = open(IMG_MAP_PATH, "w")
                    json.dump(img_map, fp)
                    fp.close()
                    text_str += "图片删除成功！"
            else:
                if command.message.has(Quote):
                    quote_message = command.message.get(Quote)[0].origin
                    if not quote_message.has(Image):
                        text_str += IMG_ERROR
                    else:
                        image = quote_message.get(Image)[0]
                        file_name = random_str()
                        await save_image(image.url, file_name)
                        command.args[0] = command.args[0].replace(BLANK_REPLACE, " ")
                        if command.args[1] == ARG_AUTO:
                            img_map[command.args[0]] = (IMG_PATH + file_name, 1)
                        elif command.args[1] == ARG_KEY:
                            img_map[command.args[0]] = (IMG_PATH + file_name, 2)
                        else:
                            img_map[command.args[0]] = (IMG_PATH + file_name, 0)
                        fp = open(IMG_MAP_PATH, "w")
                        json.dump(img_map, fp)
                        fp.close()
                        text_str += "图片添加成功！"
                elif command.args[1] == IMG_ARG_BW or command.args[1] == IMG_ARG_FLIP_UD or command.args[
                    1] == IMG_ARG_FLIP_LR \
                        or command.args[1] == IMG_ARG_ROTATE_90 or command.args[1] == IMG_ARG_ROTATE_180:

                    img_send_mode = command.args[1]
                    command.args[0] = command.args[0].replace(BLANK_REPLACE, " ")
                    if command.args[0] in img_map:
                        img_path_str += img_map[command.args[0]][0]
                    elif command.args[0].find(RANDOM_INS) == 0:
                        command.times = random_parser(command.args[0])
                        if command.times <= 0 or command.times > TIMES_LIMIT:
                            text_str = TIMES_ERROR
                        else:
                            for tim in range(command.times):
                                time.sleep(RANDOM_WAIT)
                                random.seed()
                                if tim >= 1:
                                    text_str += "\n"
                                    img_path_str += "\n"
                                img_map_list = list(img_map)
                                index = random.randint(1, len(img_map_list))
                                img_path_str += img_map[img_map_list[index - 1]][0]
                else:
                    text_str += IMG_ERROR
        else:
            text_str = ARG_ERROR

    elif command.typ == CommandType.MODE:
        if len(command.args) == 0:
            text_str += "当前模式："
            if command.mode == 0:
                text_str += MODE_NAME_NORMAL
            elif command.mode == 1:
                text_str += MODE_NAME_SILENT
            elif command.mode == 2:
                text_str += MODE_NAME_QUIET
            elif command.mode == 3:
                text_str += MODE_NAME_CRAZY
            elif command.mode == 4:
                text_str += MODE_NAME_JUDGE    
        elif len(command.args) == 1:
            text_str += "模式切换成功："
            if command.args[0] == MODE_ARG_NORMAL:
                text_str += MODE_NAME_NORMAL
            elif command.args[0] == MODE_ARG_SILENT:
                text_str += MODE_NAME_SILENT
            elif command.args[0] == MODE_ARG_QUIET:
                text_str += MODE_NAME_QUIET
            elif command.args[0] == MODE_ARG_CRAZY:
                text_str += MODE_NAME_CRAZY
            elif command.args[0] == MODE_ARG_JUDGE:
                text_str += MODE_NAME_JUDGE
            else:
                text_str = ARG_ERROR

    elif command.typ == CommandType.EXIT:
        if commander is None or commander.id == ROOT:
            text_str = OFFLINE
        else:
            text_str = PRIV_ERROR

    if img_path_str != "":
        paths = img_path_str.split("\n")
        if img_send_mode == "":
            for path in paths:
                sender.append(Image.fromLocalFile(path))
        else:
            for path in paths:
                tmp_img = PIL_IM.open(path)
                if img_send_mode == IMG_ARG_BW:
                    tmp_img = tmp_img.convert("L")
                elif img_send_mode == IMG_ARG_ROTATE_90:
                    tmp_img = tmp_img.rotate(90)
                elif img_send_mode == IMG_ARG_ROTATE_180:
                    tmp_img = tmp_img.rotate(180)
                elif img_send_mode == IMG_ARG_FLIP_UD:
                    tmp_img = tmp_img.transpose(PIL_IM.FLIP_TOP_BOTTOM)
                elif img_send_mode == IMG_ARG_FLIP_LR:
                    tmp_img = tmp_img.transpose(PIL_IM.FLIP_LEFT_RIGHT)
                tmp_img.save(IMG_PATH + "tmp.png")
                sender.append(Image.fromLocalFile(IMG_PATH + "tmp.png"))

    if at_id > 0:
        sender.append(At(at_id))
        if command.times > 1 and text_str != TIMES_ERROR:
            sender.append(Plain("\n" + text_str))
        else:
            sender.append(Plain(" " + text_str))
    else:
        sender.append(Plain(text_str))
    return sender
