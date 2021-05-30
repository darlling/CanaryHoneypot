# -*- coding:utf-8 -*-
""" 获取白名单ip """

# from dbs.dal.LogOperate import LogOp
from service.whiteipservice import whiteips
from util.auth import jwtauth

from handlers.base import BaseHandler


@jwtauth
class WhiteiplistHandler(BaseHandler):
    """获取白名单ip列表"""

    def get(self):
        res = ",".join(whiteips())
        # json.dumps(line_res)
        self.write(res)
