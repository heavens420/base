import os
import re
import time
import datetime
from datetime import timedelta
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pymysql

'''
    备份接口机服务器执行脚本
'''


# 生成本地md5校验文件  和当前账期目录
def gen_local_md5(data_type):
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    md5_file_name = str(now) + ".md5.txt"
    cmd = f"md5sum -b * > ./{md5_file_name}"

    dir_name = gen_local_dir(data_type)
    if not os.path.isfile(md5_file_name):
        os.system(cmd)
    if not os.path.isfile(now):
        gen_local_dir(now)
    return md5_file_name, dir_name


# 根据当前时间生成账期目录
def gen_local_dir(data_type):
    # 当前时间
    now = datetime.datetime.now()
    # 当月第一天
    month_one = datetime.datetime(now.year, now.month, 1)
    # 本周第一天
    week_one = now - timedelta(days=now.weekday())

    # 获取备份周期
    sql = f"select back_cycle from t_back_config where data_type_eng = f{data_type}"

    dir_prefix = exec_sql_fetchone(sql)
    if dir_prefix == '日':
        prefix = 'D'
        local_dir = now.strftime("%Y%m%d000000")
    elif dir_prefix == '周':
        prefix = 'W'
        local_dir = week_one.strftime("%Y%m%d000000")
    elif dir_prefix == '月':
        prefix = 'M'
        local_dir = month_one.strftime("%Y%m%d000000")
    else:
        # 比如说 3天 5天10天的情况
        one_format = datetime.datetime.strptime(month_one, '%Y%m%d%H%M%S')
        now_format = datetime.datetime.strptime(now, '%Y%m%d%H%M%S')
        sub_day = datetime.timedelta(days=(now_format - one_format).days % dir_prefix)
        result_day = now_format - sub_day
        local_dir = result_day.strftime('%Y%m%d000000')
        prefix = dir_prefix
    target_dir = prefix + local_dir
    os.mkdir(target_dir)
    return target_dir


def exec_sql_fetchall(sql):
    cursor, conn = con()
    cursor.execute(sql)
    lst = cursor.fetchall()
    return lst


def exec_sql_fetchone(sql):
    cursor, conn = con()
    cursor.execute(sql)
    one = cursor.fetchone()
    return one


# 生成数据类型文件夹
def gen_data_type_dir():
    cursor, conn = con()
    sql = f"select date_type_eng from t_back_config where create_time > DATE_SUB(NOW(),INTERVAL 25 HOUR) order by create_time desc;"
    cursor.execute(sql)
    date_list = cursor.fetchall()
    for item in date_list:
        if not os.path.exists(item):
            os.mkdir(item)


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


def write_upload_log(file_list):
    cursor, conn = con()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in file_list:
        file_name = item[1]
        data_type = file_name.split(".")[0]
        # cmd = f"wc -c {file_name}"
        # result = os.popen(cmd)
        # size = result.read().split(" ")[0]
        size = os.path.getsize(file_name)
        sql = f"select back_cycle,keep_time,data_type_chn from t_back_config where data_type_chn = {data_type}"
        cursor.execute(sql)
        back_config = cursor.fetchone()
        sql2 = f"insert into t_back_log(back_cycle,keep_time,data_type_chn,file_name,back_begin_date,file_size,status_cd,send_count) " \
               f"values ({back_config[0]},{back_config[1]},{back_config[2]},{file_name},{str(now)},{size},1)"
        cursor.execute(sql2)
    conn.close()


def handle_check_success(file_list):
    for file in file_list:
        cmd = f"scp ./{file[1]} xxx@xxxx:/xxx/"
        os.system(cmd)
    write_upload_log(file_list)


class Collect(object):
    def __init__(self, path):
        self.path = path
        # self.md5 = md5
        self.upload_fail_num = 0

    # 获取md5校验文件信息
    def read_file(self, md5_file):
        with open(md5_file, "r") as file:
            return file.readlines()

    # 处理md5文件 返回列表
    def get_md5_set(self, md5_file):
        file_set = set()
        lines_list = self.read_file(md5_file)

        for item in lines_list:
            file_item = str(item).replace("\n", "").replace("*", "").split(" ")
            file_set.add(file_item)
        return file_set

    # 监控是否有md5文件生成 生成即认为已经完全收到所有文件
    def monitor_file(self):
        path = r'C:\Users\420\Desktop\source\DjangoFirst'
        for root, dirs, files in os.walk(self.path):
            for file in files:
                reg = r'20\d{12}\.md5\.txt'
                result = re.match(reg, file)
                if result:
                    # print(file)
                    return file

    # 将上传失败的文件名称写入文件
    def gen_file(self, diff_list, file_name):
        with open(file_name, "a+") as file:
            for item in diff_list:
                name = item[1]
                file.write(name)

    # 处理MD5校验失败的文件
    def handle_check_failed(self, diff_list):
        # 上传失败的文件清单名称
        file_name = 'fail_upload_files.txt'
        # 生成校验失败文件清单
        self.gen_file(diff_list, file_name)
        email_receiver = "zhaolx521@gmail.com"
        title = "备份失败通知"
        message = "文件校验失败清单见附件，请重新上传"
        # 发送邮件
        send_email(email_receiver, title, message, file_name)
        # 删除生成的校验失败文件清单
        res = os.system(f"rm -fr ./{file_name}")
        # 如果没删掉再删一次，如果还删不掉 几乎不可能
        if res != 0:
            os.system(f"rm -fr ./{file_name}")

    # 文件上传
    def upload_files(self, md5_file):
        # 获取上传的md5文件名称
        # md5_file = self.monitor_file()

        # 获取上传的md5文件信息列表
        md5_set = self.get_md5_set(md5_file)
        data_type = str(md5_set[0][0]).split(".")[0]
        # 获取本地生成的md5文件名称
        local_md5_file, local_dir = gen_local_md5(data_type)

        # 生成本地md5文件列表
        local_md5_set = self.get_md5_set(local_md5_file)
        # 获取本次上传文件列表与本地生成的文件列表的差集
        compare_result = md5_set - local_md5_set
        # 如果本次上传的文件列表是本地生成校验文件列表的子集 则认为上传接收成功
        # 如果只有部分文件校验成功则上传部分文件
        success_list = md5_set - compare_result
        # 先将账期空目录上传到备份服务器
        cmd = f"scp -P 55555 -r {local_dir} xx@xx/xx/"
        os.system(cmd)
        # 将系统侧所有上传的文件 复制到存储服务器
        handle_check_success(success_list)
        # 最后上传重命名后的md5文件 备份服务器监控到改名后的md5文件则认为 备份文件接收完成
        cmd = f"scp ./{md5_file} xx@xx:/xx/upload-{md5_file}"
        os.system(cmd)
        if success_list != set():
            # 存在部分文件未上传成功或校验失败
            self.handle_check_failed(compare_result)


if __name__ == '__main__':
    c = Collect("./", "2")
    # gen_local_md5()
    # monitor_file()
    # gen_local_dir("月")

    while 1:
        file_name = c.monitor_file()
        if file_name is not None:
            time.sleep(30)
            c.upload_files(file_name)
