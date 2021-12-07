import os
import re
import datetime
import time
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
    port = 3313
    username = 'root'
    passwd = 'ROOT#'
    db = 'data_back'
    # with pymysql.connect(host=host, port=port, user=username, password=passwd, database=db, charset="utf8") as conn:
    conn = pymysql.connect(host=host, port=port, user=username, password=passwd, database=db, charset="utf8")
    # print(conn)
    conn.select_db("data_back")
    cursor = conn.cursor()
    return cursor, conn


def send_email(to, title, message, file):
    username = "heavens420@163.com"
    passwd = "VIJAZVONSXDJBTBP"
    mail_server = "smtp.163.com"
    mail_port = 465

    # to = "zhao.longlong@ustcinfo.com"

    content_apart = MIMEText(message, "plain", _charset="utf-8")
    multipart = MIMEMultipart()
    multipart.attach(content_apart)
    multipart['Subject'] = title
    # 邮件发送者
    multipart["From"] = username
    # 邮件接收者
    multipart["To"] = to

    # 附件部分
    if file is not None and file != '' and file != 'None':
        text_apart = MIMEApplication(open(file, "rb").read())
        text_apart.add_header("Content-Disposition", "attachment", filename=file)
        multipart.attach(text_apart)

    with SMTP_SSL(mail_server, mail_port) as smtp:
        smtp.login(username, passwd)
        smtp.sendmail(username, to, multipart.as_string())

    # 将上传失败的文件名称写入文件


def gen_file(diff_list, file_name):
    with open(file_name, "a+") as file:
        for item in diff_list:
            name = item[1]
            file.write(name)


# 监控接口机上传的 20xxx.md5-upload.txt文件,同时删除20xxx.md5.txt文件
def monitor_file(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            reg = r'20\d{12}\.md5-upload\.txt'
            # reg2 = r'20\d{12}\.md5\.txt'
            result = re.match(reg, file)
            if result:
                full_path = os.path.join(root, file)
                return full_path


# 获取md5校验文件信息
def read_file(md5_file):
    with open(md5_file, "r") as file:
        return file.readlines()


# 处理md5文件 返回列表 包括文件名称和其md5值
def get_md5_set(md5_file):
    file_set = set()
    lines_list = read_file(md5_file)
    for item in lines_list:
        file_item = tuple(str(item).replace("\n", "").replace("*", "").split("  "))
        file_set.add(file_item)
    return file_set


# 生成本地md5校验文件  和当前账期目录
def gen_local_md5():
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    md5_file_name = str(now) + ".md5.txt"
    cmd = f"md5sum * > ./{md5_file_name}"
    try:
        os.system(cmd)
    except Exception as e:
        print(f"生成本地md5文件异常：{e}")
    return md5_file_name


# 备份完成的文件更新数据库记录
def update_log(file, zq, sys_id):
    cursor, conn = con()
    finish_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = f"update t_back_log set back_finish_date = '{finish_date}',status_cd = 0 where file_name = '{file}' and sys_name_eng = '{sys_id}' and zq = '{zq}' and status_cd = 2"
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()


# 处理校验失败的文件 重新到接口机拉取文件
def handle_fail_files(fail_list, sys_id, data_type, zq_dir):
    for file_name in fail_list:
        cmd = f"scp -P 54321 root@jing.tk:/usr/local/my/upload/{sys_id}/{data_type}/{zq_dir}/{file_name[1]} ./"
        os.system(cmd)


# 删除校验成功的接口机上的对应文件
def handle_success_files(file, zq_dir, data_type, sys_id):
    cmd = f"ssh -p 54321 root@jing.tk rm -fr /usr/local/my/upload/{sys_id}/{data_type}/{zq_dir}/{file}"
    res = os.system(cmd)
    print(res)


def compare_md5(md5_file, fail_count=0):
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
    # 　获取 系统编码 数据类型 帐期目录
    zq_dir = current_path[len(current_path) - 1]
    data_type = current_path[len(current_path) - 2]
    sys_id = current_path[len(current_path) - 3]

    # 截取当前账期名称 20120909123456
    reg = r"(20\d{12}).md5-upload.txt"
    zq = re.search(reg, md5_file).group(1)

    for file in success_set:
        print(111)
        update_log(file[1], zq, sys_id)
        handle_success_files(file[1], zq_dir, data_type, sys_id)

    # 删除本地生成的md5文件
    os.remove(local_md5)

    # 校验失败处理
    while fail_set != set():
        fail_count += 1

        if fail_count >= 11:
            email_receiver = "zhaolx521@gmail.com"
            title = f"备份服务器备份异常"
            message = f"{sys_id}的数据类型为{data_type}帐期为{zq}的数据从接口机备份到备份服务器异常，请手动处理。异常文件见附件。"
            # 生成附件的名称
            file_name = f"{sys_id}-{data_type}-{zq}.txt"
            gen_file(fail_set, file_name)
            send_email(email_receiver, title, message, file_name)
            # 删除本地生成的附件
            os.remove(file_name)
            break

        time.sleep(60)
        # 重新拉取失败的文件
        handle_fail_files(fail_set, sys_id, data_type, zq_dir)
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
            update_log(item[1], zq, sys_id)
            handle_success_files(item[1], zq_dir, data_type, sys_id)
        os.remove(new_local_md5)

    # 比较结束 重命名接口机上传的md5文件名称 防止被二次扫描
    # now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    os.rename(md5_file, str(md5_file).replace("upload", "release"))


if __name__ == '__main__':
    while 1:
        file = monitor_file(r"/usr/local/data_back/store/")
        if file is not None:
            # 获取当前捕获的md5文件全路径
            current_path = os.path.dirname(file)
            # 进入到该路径
            os.chdir(current_path)

            compare_md5(file)

        time.sleep(600)
