# -*- coding: utf-8 -*-
# import settings
import os
import platform
import logging as lg
from hdfs.client import Client
from hdfs.client import _logger


# 记录日志（用了hdfs中源码的logger）
# logdir = settings.LOG_DIR
# _logger.setLevel(lg.DEBUG)
# myhandler = lg.FileHandler(logdir, "w")  # 覆盖模式输出日志
# myhandler.setLevel(lg.DEBUG)
# formatter = lg.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# myhandler.setFormatter(formatter)
# _logger.addHandler(myhandler)
#

class Transfer(object):

    def __init__(self):
        # self.host = settings.HOST
        # self.remotepath = settings.REMOTE_PATH
        # self.localpath = settings.LOCAL_PATH
        # self.rootpath = settings.ROOT_PATH
        self.remotepath = r'/user/root/upload'
        self.localpath = r'C:\Users\420\Downloads\Documents'
        self.rootpath = r'/user/root'
        self.host = 'http://192.168.123.205:50020'

        self.client = Client(self.host, root=self.rootpath)

    def upload_file_windows(self):
        """windowsserver"""
        try:
            base_dir = self.localpath.split('\\').pop()  # 要上传的路径的最后一个文件夹

            for root, dirs, files in os.walk(self.localpath):

                new_dir = base_dir + root.split(base_dir).pop().replace('\\','/')  # 去除本地路径前缀


                for file in files:
                    old_path = root + '\\' + file  # 原始本地路径文件
                    lpath = new_dir + '/' + file  # 去除本地路径前缀后的文件

                    if not self.client.status(self.remotepath + '/' + lpath, strict=True):

                        # 第一个参数远程路径，第二个参数本地路径，第三个参数是否覆盖，第四个参数工作线程数
                        self.client.upload(self.remotepath + '/' + lpath, old_path, overwrite=False)

        except Exception as e:
            with open("err.log", "a") as f:
                f.write(str(e))

    def upload_file_linux(self, sep):
        """linuxserver"""
        try:
            base_dir = self.localpath.split(sep).pop()  # 要上传的路径的最后一个文件夹

            for root, dirs, files in os.walk(self.localpath):

                new_dir = base_dir + root.split(base_dir).pop()  # 去除本地路径前缀

                for file in files:
                    old_path = root + sep + file  # 原始本地路径文件
                    lpath = new_dir + sep + file  # 去除本地路径前缀后的文件

                    if not self.client.status(self.remotepath + sep + lpath, strict=False):

                        # len(old_path.split("/"))
                        # 第一个参数远程路径，第二个参数本地路径，第三个参数是否覆盖，第四个参数工作线程数
                        self.client.upload(self.remotepath + sep + lpath, old_path, overwrite=False)
        except Exception as e:
            with open("err.log", "a") as f:
                f.write(str(e))


if __name__ == "__main__":
    transfer = Transfer()
    # windows server
    if platform.platform().startswith("Windows"):
        transfer.upload_file_windows()
    else:
        # linux server
        transfer.upload_file_linux('/')
