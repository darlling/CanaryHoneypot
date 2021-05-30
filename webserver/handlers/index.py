# -*- coding:utf-8 -*-
""" 后台面板首页路由 """

# from util.auth import jwtauth

from handlers.base import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):
        # Contains user found in previous auth
        self.render("index.html")

    def post(self):
        # Contains user found in previous auth
        self.render("index.html")
