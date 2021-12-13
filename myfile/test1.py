import os
import re
import time
import datetime
import traceback
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
    path_list = str(path).split("/")
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
    dir_name = ''
    try:
        # 获取系统路径和md5名称和全路径
        sys_path, md5_real_name, sys_id = get_sys_path(md5_path)
        # 先进入到指定系统路径再生成md5文件 防止生成的md5文件带有全路径 便于和系统侧生成的md5比较
        cmd = f"md5sum * > ./{md5_file_name}"

        # 截取当前账期名称 20120909123456
        reg = r"(20\d{12}).md5.txt"
        upload_time = re.search(reg, md5_real_name).group(1)

        print(os.getcwd())
        if not os.path.isfile(md5_file_name):
            result = os.system(cmd)
            print(f"49:{result}")
        dir_name = gen_local_dir(sys_id, data_type, upload_time)

        return md5_file_name, dir_name, upload_time, sys_id
    except Exception as e:
        traceback.print_exc()
        # 出現異常 就刪除本地md5文件
        os.remove(md5_file_name)
        os.rmdir(dir_name)
        print(f"生成本地md5文件异常：{e}")


# 根据当前时间生成账期目录
def gen_local_dir(sys_id, data_type, now):
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
        prefix = 'D'
        local_dir = now.strftime("%Y%m%d000000")
    elif back_cycle == '周':
        prefix = 'W'
        local_dir = week_one.strftime("%Y%m%d000000")
    elif back_cycle == '月':
        prefix = 'M'
        local_dir = month_one.strftime("%Y%m%d000000")
    else:
        month_one = month_one.strftime("%Y%m%d000000")
        now = now.strftime("%Y%m%d000000")
        # 比如说 3天 5天10天的情况
        one_format = datetime.datetime.strptime(month_one, '%Y%m%d%H%M%S')
        now_format = datetime.datetime.strptime(now, '%Y%m%d%H%M%S')
        sub_day = datetime.timedelta(days=(now_format - one_format).days % int(back_cycle[0]))
        result_day = now_format - sub_day
        local_dir = result_day.strftime('%Y%m%d000000')
        prefix = back_cycle
    target_dir = str(prefix[0]) + local_dir
    # 切换目录 创建账期文件夹
    # os.chdir("/" + sys_path)
    # print(os.getcwd())
    if not os.path.exists(target_dir):
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


def write_upload_log(file_list, sys_id, data_type, zq):
    cursor, conn = con()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = f"select back_cycle,keep_time,data_type_eng from t_back_config where data_type_eng = '{data_type}' and sys_name_eng = '{sys_id}'"
    cursor.execute(sql)
    back_config = cursor.fetchone()

    # 遍历上传成功的文件列表 添加日志
    for item in file_list:
        file_name = item[1]
        # if file_name.startswith(data_type):
            
        size = os.path.getsize(file_name)

        sql2 = f"insert into t_back_log(sys_name_eng,back_cycle,keep_time,data_type_eng,file_name,back_begin_date,file_size,zq,status_cd,send_count,md5) " \
               f"values ('{sys_id}','{back_config[0]}','{back_config[1]}','{back_config[2]}','{file_name}','{str(now)}',{size},'{zq}',2,0,'{item[0]}') "
        print(sql2)
        cursor.execute(sql2)

    conn.commit()
    conn.close()


# 遍历列表 逐个将文件上传到备份服务器
def handle_check_success(file_list, sys_id, data_type, local_dir, zq):
    for file in file_list:
        # if file[1].startswith(data_type):

        cmd = f"scp  -P 54321 ./{file[1]} root@jing.tk:/usr/local/my/upload/{sys_id}/{data_type}/{local_dir}/{file[1]}"
        os.system(cmd)
    # 同时更新日志
    write_upload_log(file_list, sys_id, data_type, zq)


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
        if md5_file is not None:
            lines_list = self.read_file(md5_file)
        else:
            return

        for item in lines_list:
            file_item = tuple(str(item).replace("\n", "").replace("*", "").split("  "))
            file_set.add(file_item)
        return file_set

    # 监控是否有md5文件生成 生成即认为已经完全收到所有文件
    def monitor_file(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                reg = r'.*20\d{12}\.md5\.txt'
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
    def handle_check_failed(self, diff_list, sys_id, zq):
        # 上传失败的文件清单名称
        file_name = f'{sys_id}-{zq}.txt'
        # 生成校验失败文件清单
        self.gen_file(diff_list, file_name)
        email_receiver = "zhaolx521@gmail.com"
        title = "系统侧上传的文件异常通知"
        message = f"{sys_id}系统的{zq}帐期文件部分文件损坏，请重新上传"
        # 发送邮件
        send_email(email_receiver, title, message, file_name)
        # 删除生成的校验失败文件清单
        os.remove(file_name)

    def is_exist_zq(self, sys_id, data_type, zq):
        cursor, conn = con()
        sql = f"select zq from t_back_log where sys_name_eng = '{sys_id}' and data_type_eng = '{data_type}' and zq = '{zq}' and status_cd = 0 limit 1"
        cursor.execute(sql)
        is_exist = cursor.fetchone()
        return is_exist

    # 根據文件類型創建文件夾 並返回文件夾名稱集合
    def get_all_date_type(self, file_list):
        data_type_set = set()
        for item in file_list:
            # 獲取文件名稱的前綴 即爲文件類型
            data_type = str(list(item)[1]).split(".")[0]
            data_type_set.add(data_type)
            # 不存在才創建
            if not os.path.isdir(data_type):
                os.mkdir(data_type)
        return data_type_set

    # 文件上传
    def upload_files(self, md5_file):
        if md5_file is None:
            return
        # 获取上传的md5文件名称
        # md5_file = self.monitor_file()

        # 获取上传的md5文件信息列表
        md5_set = self.get_md5_set(md5_file)
        data_type = str(list(md5_set)[len(md5_set) - 1][1]).split(".")[0]

        local_md5_file = ''
        local_dir = ''
        try:
            # 获取本地生成的md5文件名称和账期文件夹
            local_md5_file, local_dir, zq, sys_id = gen_local_md5(data_type, md5_file)

            # 生成本地md5文件列表
            local_md5_set = self.get_md5_set(local_md5_file)
            os.remove(local_md5_file)

            # 获取本次上传文件列表与本地生成的文件列表的差集
            compare_result = md5_set - local_md5_set
            # 如果本次上传的文件列表是本地生成校验文件列表的子集 则认为上传接收成功
            # 如果只有部分文件校验成功则上传部分文件
            success_list = md5_set - compare_result
            is_exist_zq = self.is_exist_zq(sys_id, data_type, zq)
            if is_exist_zq is None:
                # 先将账期空目录上传到备份服务器
                cmd2 = f"scp -P 54321 -r ./{local_dir} root@jing.tk:/usr/local/my/upload/{sys_id}/{data_type}"
                cmd = f"scp -P 54321 -r ./{local_dir} root@jing.tk:/usr/local/my/upload/{sys_id}/{data_type}  && rm -fr {local_dir}"
                print(cmd)
                kk = os.system(cmd2)
                print(kk)

                ss = os.system(cmd)
                if ss != 0:
                    os.rmdir(local_dir)
                    return
                print(f"290:{ss}")

            if success_list != set():
                # 将系统侧所有上传的文件 复制到存储服务器
                handle_check_success(success_list, sys_id, data_type, local_dir, zq)

                # 最后上传重命名后的md5文件 备份服务器监控到改名后的md5文件则认为 备份文件接收完成
                # 修改md5文件名称+upload标识字符串 防止二次扫描
                upload_md5_file = str(md5_file).replace(".md5.txt", ".md5-upload.txt")
                os.rename(md5_file, upload_md5_file)
                cmd = f"scp -P 54321 {upload_md5_file} root@jing.tk:/usr/local/my/upload/{sys_id}/{data_type}/{local_dir}/ && rm -rf ./{upload_md5_file}"
                res = os.system(cmd)
                if res != 0:
                    os.rmdir(local_dir)
                    return
                print(f"298:{res}")

            if compare_result != set():
                # time.sleep(3600)
                # 存在部分文件未上传成功或校验失败
                self.handle_check_failed(compare_result, sys_id, zq)

        except Exception as e:
            traceback.print_exc()
            os.remove(local_md5_file)
            os.rmdir(local_dir)
            print(f"讀取本地生成的md5文件異常：{e}")


if __name__ == '__main__':
    c = Collect()
    while 1:
        # try:
        file_name = c.monitor_file(r"/usr/local/data_back/")
        if file_name is not None:
            # 获取当前捕获的md5文件全路径
            current_path = os.path.dirname(file_name)
            # 进入到该路径
            os.chdir(current_path)
            # time.sleep(30)
            c.upload_files(file_name)
        # except Exception as e:

        # print(e)
