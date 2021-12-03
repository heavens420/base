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
    数据采集  备份接口机服务器执行脚本
'''


# 根据md5文件路径获取其父级全路径和系统编码
def get_sys_path(path):
    path_list = str(path).split("\\")
    # 获取md5文件名称不包含全路径
    md5_real_name = path_list[len(path_list) - 1]
    # 获取系统编码
    sys_id = path_list[len(path_list) - 2]
    res = ""
    for i in range(len(path_list) - 1):
        res = os.path.join(res, path_list[i])
    return res, md5_real_name, sys_id


# 生成本地md5校验文件  和当前账期目录
def gen_local_md5(data_type, md5_path):
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    md5_file_name = str(now) + ".md5.txt"
    # 获取系统路径和md5名称(不含全路径)
    sys_path, md5_real_name, sys_id = get_sys_path(md5_path)
    # 先进入到指定系统路径再生成md5文件 防止生成的md5文件带有全路径 便于和系统侧生成的md5比较
    cmd = f" cd {sys_path}  && md5sum -b * > ./{md5_file_name}"

    # 截取当前账期名称 20120909
    reg = r"(20\d{12}).md5.txt"
    upload_time = re.search(reg, md5_real_name).group(1)
    dir_name = gen_local_dir(sys_path, sys_id, data_type, upload_time)
    if not os.path.isfile(md5_file_name):
        result = os.system(cmd)
        print(result)
    return md5_file_name, dir_name, upload_time


# 根据当前时间生成账期目录
def gen_local_dir(sys_path, sys_id, data_type, now):
    # 格式化当前字符串为日期
    now = datetime.datetime.strptime(now, "%Y%m%d%H%M%S")
    # 当月第一天
    month_one = datetime.datetime(now.year, now.month, 1)
    # 本周第一天
    week_one = now - timedelta(days=now.weekday())

    # 获取备份周期
    sql = f"select back_cycle from t_back_config where data_type_eng = '{data_type}' and sys_name_eng = '{sys_id}' and status_cd = 0"

    back_cycle = exec_sql_fetchone(sql)
    if back_cycle is None or back_cycle == '':
        print(f"找不到系统{sys_id}数据类型为{data_type}的备份周期")
        return
    if back_cycle == '日':
        prefix = '1D'
        local_dir = now.strftime("%Y%m%d000000")
    elif back_cycle == '周':
        prefix = '1W'
        local_dir = week_one.strftime("%Y%m%d000000")
    elif back_cycle == '月':
        prefix = '1M'
        local_dir = month_one.strftime("%Y%m%d000000")
    else:
        month_one = month_one.strftime("%Y%m%d000000")
        now = now.strftime("%Y%m%d000000")
        # 比如说 3天 5天10天的情况
        one_format = datetime.datetime.strptime(month_one, '%Y%m%d%H%M%S')
        now_format = datetime.datetime.strptime(now, '%Y%m%d%H%M%S')
        sub_day = datetime.timedelta(days=(now_format - one_format).days % back_cycle)
        result_day = now_format - sub_day
        local_dir = result_day.strftime('%Y%m%d000000')
        prefix = back_cycle
    target_dir = str(prefix) + local_dir
    # 切换目录 创建账期文件夹
    os.chdir(sys_path)
    os.mkdir(target_dir)
    return target_dir


def exec_sql_fetchall(sql):
    cursor, conn = con()
    cursor.execute(sql)
    lst = cursor.fetchall()
    conn.close()
    return lst


def exec_sql_fetchone(sql):
    cursor, conn = con()
    cursor.execute(sql)
    one = cursor.fetchone()
    conn.close()
    return one


# 生成数据类型文件夹
def gen_data_type_dir():
    cursor, conn = con()
    sql = f"select date_type_eng from t_back_config where create_time > DATE_SUB(NOW(),INTERVAL 25 HOUR) order by create_time desc;"
    cursor.execute(sql)
    date_list = cursor.fetchall()
    conn.close()
    for item in date_list:
        if not os.path.exists(item):
            os.mkdir(item)


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


def write_upload_log(file_list, zq):
    cursor, conn = con()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 获取当前路径父级名称 即sys_id
    parent_path = os.path.dirname(os.getcwd())
    sys_id = str(parent_path).split("/")[len(parent_path) - 1]
    # 遍历上传成功的文件列表 添加日志
    for item in file_list:
        file_name = item[1]
        data_type = file_name.split(".")[0]
        # cmd = f"wc -c {file_name}"
        # result = os.popen(cmd)
        # size = result.read().split(" ")[0]
        size = os.path.getsize(file_name)
        sql = f"select back_cycle,keep_time,data_type_eng from t_back_config where data_type_chn = '{data_type}' and sys_name_eng = '{sys_id}'"
        cursor.execute(sql)
        back_config = cursor.fetchone()
        sql2 = f"insert into t_back_log(back_cycle,keep_time,data_type_eng,file_name,back_begin_date,file_size,zq,status_cd,send_count) " \
               f"values ('{back_config[0]}','{back_config[1]}','{back_config[3]}','{file_name}','{zq}','{str(now)}',{size},1) "
        cursor.execute(sql2)
    conn.close()


# 遍历列表 逐个将文件上传到备份服务器
def handle_check_success(file_list, local_dir, zq):
    for file in file_list:
        cmd = f"scp ./{file[1]} xxx@xxxx:/xxx/{local_dir}/"
        os.system(cmd)
    # 同时更新日志
    write_upload_log(file_list, zq)


class Collect(object):
    def __init__(self):
        # self.path = path
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
            file_item = tuple(str(item).replace("\n", "").replace("*", "").split(" "))
            file_set.add(file_item)
        return file_set

    # 监控是否有md5文件生成 生成即认为已经完全收到所有文件
    def monitor_file(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                reg = r'20\d{12}\.md5\.txt'
                # reg = r'.*.pdf'

                result = re.match(reg, file)
                if result:
                    # 获取md5文件全路径
                    full_file_path = os.path.join(root, file)
                    return full_file_path

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
        data_type = str(list(md5_set)[0][1]).split(".")[0]
        # 获取本地生成的md5文件名称和账期文件夹
        local_md5_file, local_dir, zq = gen_local_md5(data_type, md5_file)

        # 生成本地md5文件列表
        local_md5_set = self.get_md5_set(local_md5_file)
        # 获取本次上传文件列表与本地生成的文件列表的差集
        compare_result = md5_set - local_md5_set
        # 如果本次上传的文件列表是本地生成校验文件列表的子集 则认为上传接收成功
        # 如果只有部分文件校验成功则上传部分文件
        success_list = md5_set - compare_result
        # 先将账期空目录上传到备份服务器
        cmd = f"scp -P 55555 -r ./{local_dir} xx@xx/xx/"
        os.system(cmd)
        # 将系统侧所有上传的文件 复制到存储服务器
        handle_check_success(success_list, local_dir, zq)
        # 最后上传重命名后的md5文件 备份服务器监控到改名后的md5文件则认为 备份文件接收完成
        cmd = f"scp ./{md5_file} xx@xx:/xx/upload-{md5_file}"
        os.system(cmd)
        if success_list != set():
            # 存在部分文件未上传成功或校验失败
            self.handle_check_failed(compare_result)


if __name__ == '__main__':
    c = Collect()
    # gen_local_md5()
    # monitor_file()
    # gen_local_dir("月")
    # lss = c.get_md5_set("./md5.txt")
    # print(lss)

    res = get_sys_path(r"C:\Users\420\Desktop")
    print(res)
    # time.sleep(1000)
    while 1:
        # try:
        file_name = c.monitor_file(r"C:\Users\420\Desktop")
        if file_name is not None:
            print(file_name)
            # time.sleep(30)
        c.upload_files(file_name)
        # except Exception as e:

        # print(e)
