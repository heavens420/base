from smtplib import SMTP_SSL
from email.mime.text import MIMEText

'''
    发送邮件并抄送
'''


username = "heavens420@163.com"
passwd = "VIJAZVONSXDJBTBP"
mail_server = "smtp.163.com"
message = "nihao python  抄送测试"
mail_receiver = 'zhaolx521@163.com, heavens420@163.com, zhao.longlong@ustcinfo.com'
chaosong_receiver = "zhao.longlong@ustcinfo.com"

# plain：简单文本  html:html标签文本
msg = MIMEText(message, 'plain', _charset="utf-8")

# 邮件主题
msg["Subject"] = '邮件主题'
# 邮件发送者
msg["From"] = username
# 邮件接收者
msg["To"] = mail_receiver
# 邮件抄送
msg["Cc"] =chaosong_receiver

smtp = SMTP_SSL(host=mail_server, port=465)
smtp.login(username, passwd)
smtp.sendmail(username, mail_receiver.split(","), msg.as_string())
smtp.close()
