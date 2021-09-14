from constant import *

ONLINE = "苏醒！" + BOT_NAME + " 已于Cent OS Lighthouse启动~"
OFFLINE = "多大点事，睡了，掰"

RANDOM_RESULT = "噔噔噔，结果是："
ARG_ERROR = "狗咩纳塞，参数格式有问题噢..."
PRIV_ERROR = "狗咩纳塞，权限不够哦..."
COMMENT_ERROR = "我不好说"
IMG_ERROR = "无图，撤"
NOT_FOUND_ERROR = "404 Not Found，请仔细检查一下~"
DONT_MATCH_ERROR = "时间格式不匹配哦~"
CNKI_ERROR = "请正确回复并且保证回复的是一篇小作文~（10~1000个字捏）"
TOO_MUCH_ERROR = "全列出来太多啦，住手！"
TIMES_ERROR = "随机次数不合法或者此命令不支持多次噢~"

TAB = "\t"

GUIDE_DOC = "Hello，我是可爱的 " + BOT_NAME + "~" \
           "\n快速上手：\n使用 " + TRIGGER + HELP_INS + " " + HELP_ARG_INS + " 查看所有支持指令， \n" \
           "使用 " + TRIGGER + HELP_INS + " <指令名> 查看指令用法~"

DETAIL_DOC =   "BOT名：" + BOT_NAME + \
               "\n开发者：" + DEVELOPER_NAME + \
               "\n技术栈：Mirai + Python-Graia" + \
               "\n目前版本：" + str(VERSION) + \
               "\nBOT敏感符号：" + TRIGGER + \
               "\n空格替代符：" + BLANK_REPLACE + \
               "\n更新日志：bot模式切换，更加舒适的体验"


HINT_DOC = "小技巧："\
           "\n" + TAB + "如果想表现命令里纯文本的空格，可以用" + BLANK_REPLACE + \
           "\n" + TAB + "r命令后可以接次数噢~ 但也不能太多" + \
           "\n" + TAB + "带*为auto类型（不需用命令格式），带^为key类型（不需全文匹配）" + \
           "\n" + TAB + "为了不整蛊，循环判定/自调用命令现在取消"


INS_DOC = "指令列表："\
          "\n" + TAB + HELP_INS + TAB + "帮助" + \
          "\n" + TAB + RANDOM_INS + TAB + "随机相关" + \
          "\n" + TAB + COMMENT_INS + TAB + "评论系统" + \
          "\n" + TAB + IMG_INS + TAB + "图库系统" + \
          "\n" + TAB + ALARM_INS + TAB + "闹钟系统" + \
          "\n" + TAB + ASOUL_INS + TAB + "A-SOUL相关" + \
          "\n" + TAB + TOUHOU_INS + TAB + "东方相关" + \
          "\n" + TAB + MODE_INS + TAB + "切换模式" + \
          "\n" + TAB + EXIT_INS + TAB + "退出(仅限master)"

MORE_DOC = "除了指令集功能以外，我还可以：" \
           "\n" + TAB + "整点报时、早安" + \
           "\n" + TAB + "连续消息复读" + \
           "\n" + TAB + "接特定怪话"

HELP_DOC = "使用格式：" + TRIGGER + HELP_INS + " <参数>" + \
           "\n参数列表：" + \
           "\n" + TAB + "(缺省)" + TAB + "自我介绍、快速上手" + \
           "\n" + TAB + HELP_ARG_INS + TAB + "查看所有指令" + \
           "\n" + TAB + "<指令名>" + TAB + "查看指令用法" + \
           "\n" + TAB + HELP_ARG_DETAIL + TAB + "查看详细信息" + \
           "\n" + TAB + HELP_ARG_MORE + TAB + "查看bot隐藏功能" + \
           "\n" + TAB + HELP_ARG_HINT + TAB + "查看小贴士"

RANDOM_DOC = "使用格式：" + TRIGGER + RANDOM_INS + " <参数>" + \
            "\n参数列表：" + \
            "\n" + TAB + "(缺省)" + TAB + "随机一个[1，100]范围的整数" + \
            "\n" + TAB + "<一字动词>" + TAB + "决定做不做" + \
             "\n" + TAB + "<正整数>" + TAB + "1dN" + \
             "\n" + TAB + "<正整数>" + TAB + "<能力值>" + TAB + "进行一次判定" + \
             "\n" + TAB + RANDOM_ARG_WORD + TAB + "来点单词" + \
             "\n" + TAB + RANDOM_ARG_GK + TAB + "理(默认)/文" + TAB + "(比较合理地)随机你的高考分数" + \
            "\n" + TAB + RANDOM_ARG_RP + TAB + "看看你的今日运势" + \
             "\n" + TAB + RANDOM_ARG_RP + TAB + ARG_LS + TAB + "查看所有宜/忌" + \
             "\n" + TAB + RANDOM_ARG_RP + TAB + "<事情>" + TAB + "往宜/忌里添加" + \
            "\n" + TAB + RANDOM_ARG_RP + TAB + DEL_ARG + TAB + "<事情>" + TAB + "从宜/忌里删除"

COMMENT_DOC = "使用格式：" + TRIGGER + COMMENT_INS + " <参数>" + \
              "\n参数列表：" + \
              "\n" + TAB + "(缺省)" + TAB + "显示当前可评论事物" + \
              "\n" + TAB + RANDOM_INS + TAB + "随机来一句" + \
              "\n" + TAB + "<事物>" + TAB + "听听bot的评论" + \
              "\n" + TAB + "<事物>" + TAB + "<评论>" + TAB + "(缺省)/" + ARG_AUTO + "/" + ARG_KEY + TAB + "新建评论" + \
              "\n" + TAB + DEL_ARG + TAB + "<事物>" + TAB + "删除评论"

ALARM_DOC = "使用格式：" + TRIGGER + ALARM_INS + " <参数>" + \
            "\n参数列表：" + \
            "\n" + TAB + "(缺省)" + TAB + "显示所有闹钟" + \
            "\n" + TAB + "<时：分>" + TAB + "<提示文字>" + TAB + "设置闹钟" + \
            "\n" + TAB + DEL_ARG + TAB + "<时：分>" + TAB + "删除闹钟"

ASOUL_DOC = "使用格式：" + TRIGGER + ASOUL_INS + " <参数>" + \
            "\n参数列表：" + \
            "\n" + TAB + "(缺省)" + TAB + "随机发病小作文" + \
            "\n" + TAB + "<人名>" + TAB + "替换名称发病小作文" + \
            "\n" + TAB + ASOUL_ARG_CNKI + TAB + "回复某人，枝网查重"

TOUHOU_DOC = "使用格式：" + TRIGGER + TOUHOU_INS + " <参数>" + \
            "\n参数列表：" + \
            "\n" + TAB + TOUHOU_ARG_ROLE + TAB + RANDOM_INS + "/" + ARG_LS + TAB + "<作品名>(可选)" + TAB + RANDOM_INS + "随机角色，" + ARG_LS + "列出清单" + \
            "\n" + TAB + TOUHOU_ARG_SC + TAB + RANDOM_INS + "/" + ARG_LS + TAB + "<角色名>(可选)" + TAB + RANDOM_INS +"随机符卡，" + ARG_LS + "列出清单"

IMG_DOC = "使用格式：" + TRIGGER + IMG_INS + " <参数>" + \
          "\n参数列表：" + \
          "\n" + TAB + "(缺省)" + TAB + "显示当前可展示图片关键字" + \
          "\n" + TAB + RANDOM_INS + TAB + "<mode>" + TAB + "随机来张" + \
          "\n" + TAB + "<图片关键字>" + TAB + "<mode>" + TAB + "看看图片" + \
          "\n" + TAB + "<图片关键字>" + TAB + "(缺省)/" + ARG_AUTO + "/" + ARG_KEY + TAB + "回复某人，添加图片" + \
          "\n" + TAB + "<图片关键字>" + TAB + DEL_ARG + TAB + "删除图片" + \
          "\n图片打开模式：<mode>" + \
          "\n" + TAB + IMG_ARG_BW + TAB + "黑白" + \
          "\n" + TAB + IMG_ARG_ROTATE_90 + TAB + "逆时针90度" + \
          "\n" + TAB + IMG_ARG_ROTATE_180 + TAB + "逆时针180度" + \
          "\n" + TAB + IMG_ARG_FLIP_UD + TAB + "上下翻转" + \
          "\n" + TAB + IMG_ARG_FLIP_LR + TAB + "左右翻转"

MODE_DOC = "使用格式：" + TRIGGER + MODE_INS + " <参数>" + \
           "\n参数列表：" + \
           "\n" + TAB + "(缺省)" + TAB + "查看当前模式" + \
           "\n" + TAB + "<mode>" + TAB + "切换模式" + \
           "\nbot模式：<mode>" + \
           "\n" + TAB + MODE_ARG_NORMAL + TAB + MODE_NAME_NORMAL + \
           "\n" + TAB + MODE_ARG_SILENT + TAB + MODE_NAME_SILENT + "，只执行指令" + \
           "\n" + TAB + MODE_ARG_QUIET + TAB + MODE_NAME_QUIET + "，关键字概率触发" + \
           "\n" + TAB + MODE_ARG_CRAZY + TAB + MODE_ARG_CRAZY + "，异常积极"

GOOD_MORNING = "又是新的一天！今天是："

GOOD_NIGHT = "这是我今天最后一次报时啦，各位好梦噢~"

EXIT_DOC = "使用格式：" + TRIGGER + EXIT_INS + " 随便什么怪话，反正我不理" + \
           "\n无参数"
