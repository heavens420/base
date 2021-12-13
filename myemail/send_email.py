from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

'''
    发送邮件并 发送附件
'''


def send_email(to, title, message, file):
    username = "heavens420@163.com"
    passwd = "ILABOBPUANWHFZVE"
    mail_server = "smtp.163.com"
    mail_port = 465

    # to = "zhao.longlong@ustcinfo.com"

    # message = "测试 附件发送"
    content_apart = MIMEText(message, "plain", _charset="utf-8")

    text_file = r"./demo1.py"
    file = text_file
    text_apart = MIMEApplication(open(file, "rb").read())
    text_apart.add_header("Content-Disposition", "attachment", filename=text_file.split("\\")[-1])

    multipart = MIMEMultipart()
    multipart.attach(content_apart)
    multipart.attach(text_apart)
    multipart['Subject'] = title
    # 邮件发送者
    multipart["From"] = username
    # 邮件接收者  發送多個用 join() 處理列表
    multipart["To"] = "".join(to)

    with SMTP_SSL(mail_server, mail_port) as smtp:
        smtp.login(username, passwd)
        smtp.sendmail(username, tuple(to), multipart.as_string())


if __name__ == '__main__':
    to = ['heavens420@163.com', 'zhao.longlong@ustcinfo.com']
    title = "multi_to test"
    message = "hahahahahah"
    file = ''
    send_email(to, title, message, file)
