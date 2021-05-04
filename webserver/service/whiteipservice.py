# -*- coding:utf-8 -*-
""" 白名单过滤 """

from dbs.dal.Whiteip import White
# import sys
# sys.path.append("..")

White_res = White()


def whiteips():
    list_ip = []
    for ip in White_res.white_ip():
        list_ip.append(ip[0])
    return list_ip
