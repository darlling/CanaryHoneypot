# -*- coding:utf-8 -*-
""" 蜜罐白名单端口表 """

# import sys
# sys.path.append("..")
from dbs.initdb import Base, DBSession, engine
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, Unicode
from sqlalchemy.orm import backref, relationship


class Whiteport(Base):
    __tablename__ = 'Whiteport'
    dst_port = Column(Integer, nullable=False, primary_key=True)


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == "__main__":
    init_db()
    #drop_db()
    # Whiteport_data = Whiteport()
    # Whiteport_data.dsr_port = 3306
    # DBSession.add(Whiteport_data)
    # DBSession.flush()
    # DBSession.commit()
    print('create Whiteport table')
