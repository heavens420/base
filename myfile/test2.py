import os
import re
import datetime
from datetime import timedelta
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pymysql

'''
    数据采集  数据备份服务器上执行此脚本
'''


def con():
    host = 'jing.tk'
    port = 3312
    username = 'root'
    passwd = 'ROOT#'
    db = 'excel'
    # with pymysql.connect(host=host, port=port, user=username, password=passwd, database=db, charset="utf8") as conn:
    conn = pymysql.connect(host=host, port=port, user=username, password=passwd, database=db, charset="utf8")
    # print(conn)
    conn.select_db("excel")
    cursor = conn.cursor()
    return cursor, conn


# 监控接口机上传的 20xxx.md5-upload.txt文件,同时删除20xxx.md5.txt文件
def monitor_file(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            reg = r'20\d{12}\.md5-upload\.txt'
            reg2 = r'20\d{12}\.md5\.txt'
            result = re.match(reg, file)
            result2 = re.match(reg2, file)
            if result2:
                os.remove(file)
            if result:
                return file


# 获取md5校验文件信息
def read_file(md5_file):
    with open(md5_file, "r") as file:
        return file.readlines()


# 处理md5文件 返回列表 包括文件名称和其md5值
def get_md5_set(md5_file):
    file_set = set()
    lines_list = read_file(md5_file)
    for item in lines_list:
        file_item = str(item).replace("\n", "").replace("*", "").split(" ")
        file_set.add(file_item)
    return file_set


# 生成本地md5校验文件  和当前账期目录
def gen_local_md5():
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    md5_file_name = str(now) + ".md5.txt"
    cmd = f"md5sum -b * > ./{md5_file_name}"
    os.system(cmd)
    return md5_file_name


# 备份完成的文件更新数据库记录
def update_log(file, sys_id):
    cursor, conn = con()
    finish_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = f"update t_back_log set back_finish_date = {finish_date},status_cd = 0 where file_name = {file}　and sys_name_eng = '{sys_id}'"
    cursor.execute(sql)
    conn.commit()
    conn.close()


# 处理校验失败的文件 重新到接口机拉取文件
def handle_fail_files(fail_list):
    for file_name in fail_list:
        cmd = f"scp xx@xx:/upload/{file_name} /xx/xx/"
        os.system(cmd)


# 删除校验成功的接口机上的对应文件
def handle_success_files(file, sys_id):
    cmd = f"ssh xx@xx rm -fr /upload/{sys_id}/{file}"
    os.system(cmd)


def compare_md5(md5_file):
    # 获取本地生成的md5文件名
    local_md5 = gen_local_md5()
    # 获取本地md5信息列表
    local_md5_set = get_md5_set(local_md5)
    # 获取上传的md5信息列表
    md5_set = get_md5_set(md5_file)
    # 获取校验失败的文件信息
    fail_set = md5_set - local_md5_set
    # 获取校验成功的文件信息
    success_set = md5_set - fail_set
    # 获取当前目录全路径
    current_path = os.getcwd().split("/")
    # 　获取当前目录名称　非全路径 即系统编码
    sys_id = current_path[len(current_path) - 1]

    for file in success_set:
        update_log(file[1], sys_id)
        handle_success_files(file[1], sys_id)

    # 校验失败处理
    while fail_set != set():
        # 删除本地生成的md5文件 后面重新生成新的
        os.remove(local_md5)
        # 重新拉取失败的文件
        handle_fail_files(fail_set)
        # 重新生成md5文件
        new_local_md5 = gen_local_md5()
        # 获取新的md5文件信息
        new_local_md5_set = get_md5_set(new_local_md5)
        # 获取新的校验失败的文件列表
        new_fail_set = fail_set - new_local_md5_set
        # 获取新的校验成功的文件列表
        new_success_set = fail_set - new_fail_set
        # 将新的校验失败的文件列表赋值给 老的校验失败列表 用于循环判断
        fail_set = new_fail_set
        for item in new_success_set:
            update_log(item[1], sys_id)
            handle_success_files(item[1], sys_id)

    # 比较结束 重命名接口机上传的md5文件名称 防止被二次扫描
    # now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    os.rename(md5_file, str(md5_file).replace("upload", "release"))


if __name__ == '__main__':
    while 1:
        file = monitor_file("/")
        if file is not None:
            # 获取当前捕获的md5文件全路径
            current_path = os.path.dirname(file)
            # 进入到该路径
            os.chdir(current_path)

            compare_md5(file)
