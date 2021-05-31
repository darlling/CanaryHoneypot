# -*- coding:utf-8 -*-
""" 蜜罐白名单端口表 """

from dbs.initdb import Base, engine
from sqlalchemy import Column, Integer


class Whiteport(Base):
    __tablename__ = "Whiteport"
    dst_port = Column(Integer, nullable=False, primary_key=True)


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == "__main__":
    init_db()
    # drop_db()
    # Whiteport_data = Whiteport()
    # Whiteport_data.dsr_port = 3306
    # DBSession.add(Whiteport_data)
    # DBSession.flush()
    # DBSession.commit()
    print("create Whiteport table")
