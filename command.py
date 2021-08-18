from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from enum import Enum
from constant import *

class CommandType(Enum):
    ERROR = 0,
    HELP = 1,
    RANDOM = 2
    COMMENT = 3
    ASOUL = 4
    TOUHOU = 5
    PIXIV = 6
    ALARM = 7
    EXIT = 8


class Command:
    typ: CommandType
    error_info: str
    args: list
    message: MessageChain

    def __init__(self, _typ, _err_info):
        self.typ = _typ
        self.error_info = _err_info
        self.args = list()


def command_parser(message: MessageChain):
    """
    check命令并分解成类型 + 参数格式

    :param message: MessageChain
    :returns: Command
    """

    if message is None or not message.has(Plain):
        return Command(CommandType.ERROR, "no plain")

    text_str = message.get(Plain)[0].asDisplay()

    if text_str is None or text_str == "":
        return Command(CommandType.ERROR, "empty text")
    
    if text_str[0] != TRIGGER:
        return Command(CommandType.ERROR, "is not a bot call")
        
    text_split = text_str.split(" ")

    ret = Command(CommandType.ERROR, "undefined command")
    ret.message =  message
    ret.error_info = "no error"

    if text_split[0] == TRIGGER + HELP_INS:
        ret.typ = CommandType.HELP
    elif text_split[0] == TRIGGER + RANDOM_INS:
        ret.typ = CommandType.RANDOM
    elif text_split[0] == TRIGGER + COMMENT_INS:
        ret.typ = CommandType.COMMENT
    elif text_split[0] == TRIGGER + TOUHOU_INS:
        ret.typ = CommandType.TOUHOU
    elif text_split[0] == TRIGGER + ASOUL_INS:
        ret.typ = CommandType.ASOUL
    elif text_split[0] == TRIGGER + PIXIV_INS:
        ret.typ = CommandType.PIXIV
    elif text_split[0] == TRIGGER + ALARM_INS:
        ret.typ = CommandType.ALARM
    elif text_split[0] == TRIGGER + ASOUL_INS:
        ret.typ = CommandType.ASOUL
    elif text_split[0] == TRIGGER + TOUHOU_INS:
        ret.typ = CommandType.TOUHOU
    elif text_split[0] == TRIGGER + EXIT_INS:
        ret.typ = CommandType.EXIT

    if len(text_split) > 1:
        for i in range(1, len(text_split)):
            ret.args.append(text_split[i])

    return ret
