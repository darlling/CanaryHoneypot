# -*- coding:utf-8 -*-
""" 白名单端口过滤 """

from dbs.dal.Whiteport import WhitePort
# import sys
# sys.path.append("..")

White_res = WhitePort()


def whiteports():
    list_port = []
    for port in White_res.select_white_port():
        list_port.append(port[0])
    return list_port


def insertports(list_port):
    for p in list_port:
        if p:
            White_res.insert_white_port(int(p))
    return True


def deleteports():
    White_res.delete_white_port()
    return True