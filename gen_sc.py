from constant import *

import json

fp = open("local/sc.txt", "r", encoding="utf-8")

spellcard = dict()

while True:
    line = fp.readline()
    print(line)
    if not line:
        break
    if line[0] == "!":
        print(line)
        role = line.replace("!TEM ", "")
        role = role.replace("符卡名", "")
        role = role.replace("Naz", "娜兹玲")
        role = role.replace("Lily", "莉莉霍瓦特")
        role = role.replace("\n", "")
        spellcard[role] = list()
    elif line[0].isalpha():
        card = line.replace("\n", "")
        spellcard[role].append(card)

for role in spellcard:
    print(role)
    print(spellcard[role])

fp.close()

fp = open(TOUHOU_SC_PATH, "w", encoding="utf-8")

json.dump(spellcard, fp)

