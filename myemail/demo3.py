from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

'''
    发送邮件并 发送附件
'''


def send_email():
    username = "heavens420@163.com"
    passwd = "VIJAZVONSXDJBTBP"
    mail_server = "smtp.163.com"
    mail_port = 465

    to = "zhao.longlong@ustcinfo.com"

    message = "测试 附件发送"
    content_apart = MIMEText(message, "plain", _charset="utf-8")

    img_file = r"/myemail\排序算法.jpg"
    img_apart = MIMEImage(open(img_file, "rb").read(), img_file.split(".")[-1])
    img_apart.add_header("Content-Disposition", "attachment", filename=img_file.split("\\")[-1])

    text_file = r"/myemail\demo1.py"
    text_apart = MIMEApplication(open(text_file, "rb").read())
    text_apart.add_header("Content-Disposition", "attachment", filename=text_file.split("\\")[-1])

    multipart = MIMEMultipart()
    multipart.attach(content_apart)
    multipart.attach(img_apart)
    multipart.attach(text_apart)
    multipart['Subject'] = '附件测试 dierci  disanci '
    # 邮件发送者
    multipart["From"] = username
    # 邮件接收者
    multipart["To"] = to

    with SMTP_SSL(mail_server, mail_port) as smtp:
        smtp.login(username, passwd)
        smtp.sendmail(username, to, multipart.as_string())


send_email()