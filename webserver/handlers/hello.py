# -*- coding:utf-8 -*-
""" 测试认证请求里的token """

from service.hostservice import hostonline

from handlers.base import BaseHandler

# from util.auth import jwtauth


# @jwtauth
class HelloHandler(BaseHandler):
    def get(self):
        print(hostonline())
        # self.write(str(hostonline()))
        self.write("ok")

        # Contains user found in previous auth
        # if self.request.headers.get('Authorization'):
        #     self.write('ok')
