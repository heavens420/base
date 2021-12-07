import datetime
import pymysql
import os
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

'''
    发送周报月报 报告备份信息
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


def gen_report():
    cursor, conn = con()
    sql = f"select con.sys_name_chn,con.data_type_chn,con.back_cycle,con.keep_time,log.file_name,log.back_finish_date,con.keep_time," \
          f"log.file_size from t_back_config con inner join t_back_log log on con.sys_name_eng = log.sys_name_eng " \
          f"where con.status_cd = 0 and log.status_cd = 0 order by con.sys_name_chn,con.data_type_chn,log.back_finish_date,log.file_size"
    print(sql)
    cursor.execute(sql)
    result_list = cursor.fetchall()
    conn.close()

    # 最终的csv文件列表
    result = []
    # csv文件名称
    csv_file = "report.csv"
    # 保存前一个系统名称
    pre_sys = ''
    # 系统备份占用磁盘总量
    dh_total = 0
    for i in range(len(result_list)):
        child = list(result_list[i])
        i += 1
        # for it in child:
        now = datetime.datetime.now()
        # 备份完成时间
        back_finish_date = str(child[5])
        back_date = datetime.datetime.strptime(back_finish_date, "%Y-%m-%d %H:%M:%S")
        # 已经备份地周期数
        delta = (now - back_date).days % int(child[2])
        # 保存已经备份的周期数
        child[5] = delta

        # 为空表名是第一行进来，占用磁盘总量就是当前文件大小
        if pre_sys == '':
            dh_total = int(child[7])
            child.append(dh_total)
        else:  # 非空说明不是第一行
            # 如果当前行的系统名称等于上一个系统名称 说明还是同一个系统 则占用总量累加
            if child[0] == pre_sys:
                dh_total += int(child[7])
                child.append(dh_total)
            else:  # 当前系统名称不等于上一个 则是一个新的系统，磁盘占用总量重新计算
                dh_total = 0
                dh_total += int(child[7])
                child.append(dh_total)
        # 把当前系统名称赋值给它 它在下一遍历时就成了前一个
        pre_sys = child[0]
        result.append(child)

    for item in result:
        item = str(item).replace("(", "").replace("'", "").replace(")", "\n") \
            .replace(" ", "").replace("[", "").replace("]", "\n")
        with open(csv_file, "a+") as cs:
            cs.write(str(item))
    return csv_file


if __name__ == '__main__':
    try:
        os.chdir("/store")
        csv_file = gen_report()
        mail_receiver = ""
        title = "系统备份周报/月报"
        message = "本周/月文件备份详情见附件"
        send_email(mail_receiver, title, message, csv_file)
    except Exception as e:
        print(e)
