# -*- coding:utf-8 -*-
""" 邮件配置增删改 """

from json import loads

from application import emailfile
from util.auth import jwtauth
from util.config import ini_info

from handlers.base import BaseHandler

ini = ini_info(emailfile)


@jwtauth
class EmailModifyHandler(BaseHandler):
    # 接收json 请求修改email配置文件

    def write_error(self, status_code, **kwargs):
        self.write("Unable to parse JSON.")

    def post(self):
        # 接收提交过来的email配置
        if self.request.headers["Content-Type"].startswith("application/json"):
            json_args = loads(self.request.body.decode("utf-8"))

            # 更新email.ini
            ini.cfg_load()
            ini.set_item("email", "user", json_args["user"])
            ini.save()
            self.write(json_args)
        else:
            self.json_args = None
            message = "Unable to parse JSON."
            self.send_error(status_code=400)  # 向浏览器发送错误状态码，会调用write_error

    def get(self):

        ini.cfg_load()

        user = ini.cfg_dump()[0][0]
        email = ini.cfg_dump()[0][1]
        email_json = {user: email}

        self.write(email_json)
