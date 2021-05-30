# -*- coding:utf-8 -*-
""" 白名单端口表操作 """

from dbs.initdb import DBSession
from dbs.models.Whiteport import Whiteport
from sqlalchemy.exc import InvalidRequestError


class WhitePort:
    """增删改查"""

    def __init__(self):
        self.session = DBSession

    # 查询白名单表port数据
    def select_white_port(self):
        try:
            white_port_res = self.session.query(Whiteport.dst_port).all()
            return white_port_res
        except InvalidRequestError:
            self.session.rollback()
        except Exception as e:
            print(e)
        finally:
            self.session.close()

    # 增加白名单
    def insert_white_port(self, dst_port):
        try:
            wip_insert = Whiteport(dst_port=dst_port)
            self.session.merge(wip_insert)
            self.session.commit()
        except InvalidRequestError:
            self.session.rollback()
        except Exception as e:
            print(e)
        finally:
            self.session.close()

    # 删除白名单端口表数据
    def delete_white_port(self):
        try:
            self.session.query(Whiteport).delete()
            self.session.commit()
        except InvalidRequestError:
            self.session.rollback()
        except Exception as e:
            print(e)
        finally:
            self.session.close()
