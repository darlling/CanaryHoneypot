# -*- coding:utf-8 -*-
""" URL路由配置文件 """

from unittest import main

from handlers import (chart, email, hello, host, index, logcollection, login,
                      paginationlog, whiteiplist, whiteport)

url = [
    # LoginHandler url
    (r"/", index.IndexHandler),
    (r"/auth/*", login.AuthHandler),
    (r"/log/*", logcollection.ReceiveJsonHandler),
    (r"/log/list/*", paginationlog.GetlistJsonHandler),
    (r"/mail/*", email.EmailModifyHandler),
    (r"/chart/*", chart.ChartHandler),
    (r"/whiteiplist/", whiteiplist.WhiteiplistHandler),
    (r"/whiteport/", whiteport.WhiteportHandler),
    (r"/host/*", host.HostHandler),
    (r"/gethost/*", host.GetHostHandler),
    (r"/hello/*", hello.HelloHandler),
    (r".*", index.IndexHandler)
    # (r"/logout", login.LogoutHandler),
]

if __name__ == "__main__":
    main()
