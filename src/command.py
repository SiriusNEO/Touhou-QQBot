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
    IMG = 6
    ALARM = 7
    MODE = 8
    EXIT = 9


class Command:
    typ: CommandType
    error_info: str
    times: int
    mode: int
    args: list
    message: MessageChain

    def __init__(self, _typ, _err_info, _message, _mode):
        self.typ = _typ
        self.error_info = _err_info
        self.message = _message
        self.args = list()
        self.times = 1
        self.mode = _mode


def random_parser(arg: str):
    arg = arg.replace(RANDOM_INS, "")
    if arg == "":
        return 1
    if not arg.isdigit():
        return 0
    return int(arg)


def command_parser(message: MessageChain, mode: int):
    """
    check命令并分解成类型 + 参数格式

    :param message: MessageChain
    :param mode: int
    :returns: Command
    """

    if message is None or not message.has(Plain):
        return Command(CommandType.ERROR, "no plain", message, mode)

    text_str = message.get(Plain)[0].asDisplay().strip()

    if text_str is None or text_str == "":
        return Command(CommandType.ERROR, "empty text", message, mode)
    
    if text_str[0] != TRIGGER:
        return Command(CommandType.ERROR, "is not a bot call", message, mode)

    ret = Command(CommandType.ERROR, "no error", message, mode)
    text_split = text_str.split(" ")

    if text_split[0] == TRIGGER + HELP_INS:
        ret.typ = CommandType.HELP
    elif text_split[0].find(TRIGGER + RANDOM_INS) != -1:
        ret.times = random_parser(text_split[0][1:])
        ret.typ = CommandType.RANDOM
    elif text_split[0] == TRIGGER + COMMENT_INS:
        ret.typ = CommandType.COMMENT
    elif text_split[0] == TRIGGER + TOUHOU_INS:
        ret.typ = CommandType.TOUHOU
    elif text_split[0] == TRIGGER + ASOUL_INS:
        ret.typ = CommandType.ASOUL
    elif text_split[0] == TRIGGER + IMG_INS:
        ret.typ = CommandType.IMG
    elif text_split[0] == TRIGGER + ALARM_INS:
        ret.typ = CommandType.ALARM
    elif text_split[0] == TRIGGER + ASOUL_INS:
        ret.typ = CommandType.ASOUL
    elif text_split[0] == TRIGGER + TOUHOU_INS:
        ret.typ = CommandType.TOUHOU
    elif text_split[0] == TRIGGER + MODE_INS:
        ret.typ = CommandType.MODE
    elif text_split[0] == TRIGGER + EXIT_INS:
        ret.typ = CommandType.EXIT
    else:
        ret.error_info = "undefined command"
    if len(text_split) > 1:
        for i in range(1, len(text_split)):
            ret.args.append(text_split[i])

    return ret
