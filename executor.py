from command import *
from illustration import *
from graia.application import *
from graia.application.group import Group, Member
from graia.application.message.elements.internal import Plain, Image, At, Quote
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


def execute(command: Command, commander: Member):
    """
    执行命令

    :param command: Command
    :param commander: 执行者
    :returns: list, 初始化 MessageChain
    """
    sender = list()
    text_str = str()
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
            elif command.args[0] == EXIT_INS:
                text_str = EXIT_DOC
            else:
                text_str = ARG_ERROR
        else:
            text_str = ARG_ERROR

    elif command.typ == CommandType.RANDOM:
        random.seed()
        if len(command.args) == 0:
            command.args.append("100")
        if len(command.args) == 1:
            if command.args[0].isdigit():
                ranger = int(command.args[0])
                result = random.randint(1, ranger)
                if commander is not None:
                    at_id = commander.id
                text_str = RANDOM_RESULT + str(result) + "d" + str(ranger)

            elif len(command.args[0]) == 1:
                todo = (random.randint(0, 1) == 1)
                if commander is not None:
                    at_id = commander.id
                if todo:
                    text_str = str(command.args[0] + "!")
                else:
                    text_str = str("不" + command.args[0] + "，算了吧...")

            elif command.args[0] == RANDOM_ARG_GK:
                chinese = int(random.gauss(120, 5))
                math = int(random.gauss(125, 15))
                english = int(random.gauss(138, 10))
                if chinese > 145:
                    chinese = 145
                if math > 149:
                    math = 150
                if english > 149:
                    english = 149
                text_str = "您参加普通高等学校招生全国统一考试的分数是：" + \
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

                text_str = "您的今日运势是：" + str(lucky) + ", " + rp_level(lucky)
                if commander is not None:
                    at_id = commander.id

                good_behavior = random.randint(1, len(BEHAVIOR))
                bad_behavior = random.randint(1, len(BEHAVIOR))

                text_str += "\n宜：" + BEHAVIOR[good_behavior - 1]
                text_str += "\n忌：" + BEHAVIOR[bad_behavior - 1]

            else:
                text_str = ARG_ERROR

        elif len(command.args) == 2:
            if command.args[0].isdigit() and command.args[1].isdigit():
                ranger = int(command.args[0])
                checker = int(command.args[1])

                result = random.randint(1, ranger)

                text_str = RANDOM_RESULT + str(result) + "d" + str(ranger) + "，"
                if commander is not None:
                    at_id = commander.id
                if result >= checker:
                    text_str += "检定失败..."
                else:
                    text_str += "检定成功!"
            elif command.args[0] == RANDOM_ARG_GK:
                chinese = int(random.gauss(120, 5))
                math = int(random.gauss(125, 15))
                english = int(random.gauss(138, 10))
                if chinese > 145:
                    chinese = 145
                if math > 149:
                    math = 150
                if english > 149:
                    english = 149
                text_str = "您参加普通高等学校招生全国统一考试的分数是：" + \
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
            for i in range(len(comments_list)):
                if i != 0:
                    text_str += "，"
                text_str += comments_list[i]
        elif len(command.args) == 1:
            if command.args[0] in comments:
                text_str += comments[command.args[0]][0]
            else:
                text_str += COMMENT_ERROR
        elif len(command.args) == 2:
            if command.args[0] == DEL_ARG:
                if command.args[1] not in comments:
                    text_str = NOT_FOUND_ERROR
                else:
                    comments.pop(command.args[1])
                    fp = open(COMMENT_PATH, "w")
                    json.dump(comments, fp)
                    fp.close()
                    text_str += "评论删除成功！"
            else:
                command.args[1] = command.args[1].replace(BLANK_REPLACE, " ")
                comments[command.args[0]] = (command.args[1], False)
                fp = open(COMMENT_PATH, "w")
                json.dump(comments, fp)
                fp.close()
                text_str += "评论添加成功！"
        elif len(command.args) == 3:
            command.args[1] = command.args[1].replace(BLANK_REPLACE, " ")
            comments[command.args[0]] = (command.args[1], command.args[2] == "auto")
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
            text_str = random_writing()
        elif len(command.args) == 1 and command.args[0] == ASOUL_ARG_CNKI:
            if not command.message.has(Quote):
                text_str = QUOTE_ERROR
            else:
                quote_message = command.message.get(Quote)[0].origin
                if not quote_message.has(Plain):
                    text_str = QUOTE_ERROR
                else:
                    origin_text = quote_message.get(Plain)[0].asDisplay()
                    if len(origin_text) < 10 or len(origin_text) > 1000:
                        text_str = QUOTE_ERROR
                    else:
                        info_dict = check_duplicate(origin_text)
                        text_str = "枝网查重报告 车车群特供版"
                        if "author" not in info_dict:
                            text_str += "\n查重率: 0%，支持原创捏"
                        else:
                            text_str += "\n" + info_dict['rate'] + \
                                        "\n" + info_dict['author'] + \
                                        "\n" + info_dict['time'] + \
                                        "\n" + info_dict['link']

        else:
            text_str = ARG_ERROR

    elif command.typ == CommandType.TOUHOU:
        if len(command.args) == 2:
            if command.args[1] == TOUHOU_ARG_LS:
                text_str = TOO_MUCH_ERROR
            elif command.args[1] == TOUHOU_ARG_RD:
                if command.args[0] == TOUHOU_ARG_ROLE:
                    result = get_role("")
                    at_id = commander.id
                    text_str = "[Touhou Role] 您抽到了："
                    text_str += "\n" + result[0]
                    text_str += "\n来自：" + result[1]
                elif command.args[0] == TOUHOU_ARG_SC:
                    result = get_sc("")
                    text_str = "[Touhou Spellcard] 您抽到了："
                    text_str += "\n" + result[0]
                    text_str += "\n使用者：" + result[1]
                else:
                    text_str = ARG_ERROR
            else:
                text_str = ARG_ERROR
        elif len(command.args) == 3:
            if command.args[1] == TOUHOU_ARG_LS:
                if command.args[0] == TOUHOU_ARG_ROLE:
                    role_list = list_role(command.args[2])
                    if len(role_list) == 0:
                        text_str = NOT_FOUND_ERROR
                    else:
                        at_id = commander.id
                        text_str = "[Touhou Role] 作品 [" + command.args[2] + "]："
                        for role in role_list:
                            text_str += "\n" + role
                elif command.args[0] == TOUHOU_ARG_SC:      
                    sc_list = list_sc(command.args[2])
                    if len(sc_list) == 0:
                        text_str = NOT_FOUND_ERROR
                    else:
                        at_id = commander.id
                        text_str = "[Touhou Spellcard] 角色 [" + command.args[2] + "]："
                        for sc in sc_list:
                            text_str += "\n" + sc
                else:
                    text_str = ARG_ERROR    
            elif command.args[1] == TOUHOU_ARG_RD:
                if command.args[0] == TOUHOU_ARG_ROLE:
                    result = get_role(command.args[2])
                    if result[0] == "":
                        text_str = NOT_FOUND_ERROR
                    else:
                        at_id = commander.id
                        text_str = "[Touhou Role] 您抽到了："
                        text_str += "\n" + result[0]
                        text_str += "\n来自：" + result[1]
                elif command.args[0] == TOUHOU_ARG_SC:
                    result = get_sc(command.args[2])
                    if result[0] == "":
                        text_str = NOT_FOUND_ERROR
                    else:
                        at_id = commander.id
                        text_str = "[Touhou Spellcard] 您抽到了："
                        text_str += "\n" + result[0]
                        text_str += "\n使用者：" + result[1]
                else:
                    text_str = ARG_ERROR
            else:
                text_str = ARG_ERROR
        else:
            text_str = ARG_ERROR

    elif command.typ == CommandType.EXIT:
        if commander is None or commander.id == ROOT:
            text_str = OFFLINE
        else:
            text_str = PRIV_ERROR

    if at_id > 0:
        sender.append(At(at_id))
        sender.append(Plain(" " + text_str))
    else:
        sender.append(Plain(text_str))
    return sender
