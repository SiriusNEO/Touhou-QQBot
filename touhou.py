from constant import *
import json
import random


def get_role(collection: str):
    fp = open(TOUHOU_ROLE_PATH, "r", encoding="utf-8")
    role_table = json.load(fp=fp)
    random.seed()
    if collection == "":
        col_list = list(role_table)
        col_index = random.randint(1, len(col_list))
        collection = col_list[col_index-1]

    if collection not in role_table:
        return "", ""

    role_list = role_table[collection]
    index = random.randint(1, len(role_list))
    return role_list[index-1], collection


def list_role(collection: str):
    fp = open(TOUHOU_ROLE_PATH, "r", encoding="utf-8")
    role_table = json.load(fp=fp)

    if collection not in role_table:
        return list()

    return role_table[collection]


def get_sc(role: str):
    fp = open(TOUHOU_SC_PATH, "r", encoding="utf-8")
    sc_table = json.load(fp=fp)
    random.seed()
    if role == "":
        role_list = list(sc_table)
        role_index = random.randint(1, len(role_list))
        role = role_list[role_index-1]
    if role not in sc_table:
        return "", ""
    sc_list = sc_table[role]
    index = random.randint(1, len(sc_list))
    return sc_list[index-1], role


def list_sc(role: str):
    fp = open(TOUHOU_SC_PATH, "r", encoding="utf-8")
    sc_table = json.load(fp=fp)

    if role not in sc_table:
        return ""
    return sc_table[role]

