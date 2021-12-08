import os
import datetime
import pymysql
import re
import time
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

'''
    数据下发功能 此脚本在下发服务器执行
'''


def con():
    host = 'jing.tk'
    port = 3313
    username = 'root'
    passwd = 'ROOT#'
    db = 'data_back'
    conn = pymysql.connect(host=host, port=port, user=username, password=passwd, database=db, charset="utf8")
    conn.select_db("data_back")
    cursor = conn.cursor()
    return cursor, conn


# 监控是否有20xxx.md5-release.txt文件生成 生成即认为已经完全收到所有文件
def monitor_file(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            reg = r'.*20\d{12}\.md5-release\.txt'
            result = re.match(reg, file)
            if result:
                full_path_file = os.path.join(root, file)
                return full_path_file


# 生成本地md5校验文件  和当前账期目录
def gen_local_md5():
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    md5_file_name = str(now) + ".md5.txt"
    cmd = f"md5sum  * > ./{md5_file_name}"
    if not os.path.isfile(md5_file_name):
        os.system(cmd)
    return md5_file_name


# 获取md5校验文件信息
def read_file(md5_file):
    with open(md5_file, "r") as file:
        return file.readlines()


# 处理md5文件 返回列表
def get_md5_set(md5_file):
    file_set = set()
    lines_list = read_file(md5_file)

    for item in lines_list:
        file_item = tuple(str(item).replace("\n", "").replace("*", "").split("  "))
        file_set.add(file_item)
    return file_set


# 更新下发记录
def write_release_log(file_list):
    cursor, conn = con()
    for item in file_list:
        finish_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = f"update t_back_log set send_count = send_count+1 where md5 = '{item[0]}'"
        sql2 = f"update t_release_log set send_finish_date = '{finish_date}' where md5 = '{item[0]}'"
        cursor.execute(sql)
        cursor.execute(sql2)
    # 更改操作 要提交
    conn.commit()
    conn.close()


# 处理校验失敗的文件
def handle_fail_file(file_list, content):
    cursor, conn = con()
    sql = f"select back_cycle from t_back_log where zq = '{content[2]}' limit 1"
    cursor.execute(sql)
    back_cycle = cursor.fetchone()

    # 獲取文件夾名稱
    zq_dir = back_cycle[0] + content[2][:8] + "000000"
    # 遍歷 失敗文件列表 重新拉取文件
    for item in file_list:
        cmd = f"scp -P 54321 root@jing.tk:/usr/local/my/upload/{content[0]}/{content[1]}/{zq_dir}/{item[1]}  ./"
        os.system(cmd)


# 发送邮件
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


def compare_md5(md5_file):
    # 获取本地生成的md5文件名称
    local_md5_file = gen_local_md5()
    # 获取本地生成的md5信息列表
    local_md5_info_list = get_md5_set(local_md5_file)
    # 获取下发的md5文件信息列表
    md5_info_list = get_md5_set(md5_file)
    # 获取校验失败的文件信息集合
    check_fail_list = md5_info_list - local_md5_info_list
    # 获取校验成功的文件信息集合
    check_success_list = md5_info_list - check_fail_list
    # 校验成功的写日志
    write_release_log(check_success_list)

    # 删除本地生成的md5文件
    os.remove(local_md5_file)

    # 获取备份服务器上要重新拉取文件的路径
    cursor, conn = con()
    sql = f"select sys_name_eng,data_type_eng,zq from t_back_log where md5 = '{list(md5_info_list)[0][0]}' limit 1"
    cursor.execute(sql)
    content = cursor.fetchone()
    conn.close()

    # 失败重新拉取文件重新校验直至成功
    if check_fail_list != set():
        # 处理校验失败的文件
        handle_fail_file(check_fail_list, content)
        # 重新比较
        compare_md5(md5_file)

    # 修改md5文件名，防止被二次扫描
    if os.path.isfile(md5_file):
        os.rename(md5_file, str(md5_file).replace(".md5-release.txt", ".md5-finish.txt"))

        email_receiver = "zhaolx521@gmail.com"
        title = f"數據下發成功通知"
        message = f"{content[0]}系统{content[2]}帐期的数据下发成功，请及时拉取。数据将在72小时后自动删除。"
        send_email(email_receiver, title, message, '')


if __name__ == '__main__':
    while 1:
        try:
            md5_file = monitor_file("/usr/local/data_back/")
            if md5_file is not None:
                current_path = os.path.dirname(md5_file)
                os.chdir(current_path)
                compare_md5(md5_file)
            time.sleep(30)
        except Exception as e:
            print(e)
