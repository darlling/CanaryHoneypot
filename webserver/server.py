# -*- coding:utf-8 -*-
""" 服务端启动文件 """

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from application import settings
from url import url
from util.task import check_scheduler

define("port", default=8888, help="run on the given port", type=int)

if __name__ == "__main__":
    check_scheduler()
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=url, **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port, address="0.0.0.0")
    print("Development server is running at http://0.0.0.0:%s/" % options.port)
    tornado.ioloop.IOLoop.instance().start()
