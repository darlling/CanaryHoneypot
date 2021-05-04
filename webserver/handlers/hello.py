# -*- coding:utf-8 -*-
""" 测试认证请求里的token """

import tornado
from service.hostservice import hostonline
from util.auth import jwtauth

from handlers.base import BaseHandler


# @jwtauth
class HelloHandler(BaseHandler):
    def get(self):
        print(hostonline())
        # self.write(str(hostonline()))
        self.write("ok")

        # Contains user found in previous auth
        # if self.request.headers.get('Authorization'):
        #     self.write('ok')
