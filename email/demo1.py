from smtplib import SMTP_SSL
from smtplib import SMTP
from email.mime.text import MIMEText


def sendMail(message, subject, sender_show, recipient_show, to_addrs, cc_show=''):
    '''
    :param message: str 邮件内容
    :param Subject: str 邮件主题描述
    :param sender_show: str 发件人显示，不起实际作用如："xxx"
    :param recipient_show: str 收件人显示，不起实际作用 多个收件人用','隔开如："xxx,xxxx"
    :param to_addrs: str 实际收件人
    :param cc_show: str 抄送人显示，不起实际作用，多个抄送人用','隔开如："xxx,xxxx"
    '''

    # 填写真实的发邮件服务器用户名、密码
    user = 'heavens420@163.com'
    # user = '1808056378@qq.com'
    password = 'VIJAZVONSXDJBTBP'
    # password = 'QQbaby223'
    # 邮件内容
    msg = MIMEText(message, 'plain', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = subject
    # 发件人显示，不起实际作用
    msg["from"] = sender_show
    # 收件人显示，不起实际作用
    msg["to"] = recipient_show
    # 抄送人显示，不起实际作用
    msg["Cc"] = cc_show
    with SMTP_SSL(host="smtp.163.com", port=465) as smtp1:
        # smtp1.debuglevel(0)
        # 登录发邮件服务器
        smtp1.login(user=user, password=password)
        # 实际发送、接收邮件配置
        smtp1.sendmail(from_addr=user, to_addrs=to_addrs, msg=msg.as_string())


if __name__ == '__main__':
    print("9999999999999999999999")
    message = 'Python让你回家吃饭'
    subject1 = '吃饭'
    # 显示发送人
    sender_show = 'heavens420@163.com'
    # 显示收件人
    recipient_show = 'zhaolx521@163.com'
    # 实际发给的收件人
    to_addrs = ['zhaolx521@163.com']
    try:
        sendMail(message, subject1, sender_show, recipient_show, to_addrs)
    except Exception as e:
        print(e)
