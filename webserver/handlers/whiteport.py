# -*- coding:utf-8 -*-
""" 获取白名单port """

# from dbs.dal.LogOperate import LogOp
from json import loads

from service.whiteportservice import deleteports, insertports, whiteports
from util.auth import jwtauth

from handlers.base import BaseHandler


@jwtauth
class WhiteportHandler(BaseHandler):
    """获取白名单port列表"""

    def get(self):
        # res = ''
        res = ",".join("%s" % p for p in whiteports())
        # json.dumps(line_res)
        self.write(res)

    def write_error(self, status_code, **kwargs):
        self.write("Unable to parse JSON.")

    def post(self):
        # 接收提交过来的port
        if self.request.headers["Content-Type"].startswith("application/json"):
            json_args = loads(self.request.body.decode("utf-8"))
            port_list = json_args["port"].split(",")
            if port_list:
                deleteports()
                insertports(port_list)
            self.write(json_args)
        else:
            self.json_args = None
            message = "Unable to parse JSON."
            self.send_error(status_code=400)  # 向浏览器发送错误状态码，会调用write_error
