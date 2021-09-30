import os, time, sys


class MysqlBack(object):
    def __init__(self, user_name, passwd, host, database):
        self.user_name = user_name
        self.passwd = passwd
        self.host = host
        self.database = database

    def dump(self):
        os.system("mysqldump -u%s -p%s -h%s %s")
