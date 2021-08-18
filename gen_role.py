from constant import *

import json

fp = open("local/role.txt", "r", encoding="utf-8")

collection = dict()

game = "主角二人组"

def is_Chinese(ch):
    if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

while True:
    line = fp.readline()
    if not line:
        break
    if line[0] == "=":
        game = ""
        for ch in line:
            if is_Chinese(ch) or ch.isalpha():
                game += ch
        collection[game] = list()
    elif line[0] == "*":
        content = line.replace("[", "")
        content = content.replace("]", "")
        content = content.replace("* ", "")
        content = content.replace("*", "")
        content = content.replace("\n", "")
        content = content.replace("{", "")
        content = content.replace("}", "")
        content = content.replace("c ", "")
        content = content.replace("x ", "")
        content = content.replace("naz", "娜兹玲")
        content = content.replace("Lily", "莉莉霍瓦特")
        collection[game].append(content)


print("display")

collection.pop("旧作")
collection.pop("音乐CD及出版品")

for game in collection:
    print(game)
    flag = True
    while flag:
        flag = False
        for i in range(len(collection[game])):
            if collection[game][i].find("其他角色") != -1:
                collection[game].pop(i)
                flag = True
                break
    print(collection[game])

fp.close()
fp = open(TOUHOU_ROLE_PATH, "w", encoding="utf-8")

json.dump(collection, fp)
