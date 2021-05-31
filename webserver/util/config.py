# -*- coding:utf-8 -*-
""" 邮件、白名单配置 """

import sys
from configparser import ConfigParser

sys.path.append("..")
from application import emailfile


class ini_info(object):
    def __init__(self, recordfile):
        self.logfile = recordfile
        self.cfg = ConfigParser()

    def cfg_load(self):
        self.cfg.read(self.logfile)

    def cfg_dump(self):
        se_list = self.cfg.sections()
        # print('='*30)
        for se in se_list:
            # print 'a'
            # print(se)
            # print 'b'
            # print(self.cfg.items(se))
            # self.cfg.items(se)
            # print('='*30)
            return self.cfg.items(se)

    def cfg_get(self, section, option):
        v = self.cfg.get(section, option)
        print(v)
        return v

    def delete_item(self, section, key):
        self.cfg.remove_option(section, key)

    def delte_section(self, section):
        self.cfg.remove_section(section)

    def add_section(self, section):
        self.cfg.add_section(section)

    def set_item(self, section, key, value):
        self.cfg.set(section, key, value)

    def save(self):
        with open(self.logfile, "w") as fp:
            self.cfg.write(fp)


if __name__ == "__main__":
    ini = ini_info(emailfile)
    ini.cfg_load()
    ini.cfg_dump()

    ini.set_item("email", "user", "1356358689@qq.com")
    ini.cfg_dump()
    ini.cfg_get("email", "switch")

    # ini.add_section('rose')
    # ini.set_item('rose', 'pwd', 'ccc')
    # ini.set_item('rose', 'port', '8080')
    # ini.cfg_dump()

    # ini.delte_section('tom')
    # ini.cfg_dump()

    ini.save()
