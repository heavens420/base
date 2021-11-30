from ftplib import FTP_TLS
from ftplib import FTP


def conn():
    # with FTP_TLS() as ftp:
    # ftp = FTP_TLS(host='jing.tk:21', user='ftpuser', passwd="ftpuser123")
    ftp = FTP()
    # 调试信息 默认0 最高2 等级越高打印的日志越多
    # ftp.set_debuglevel(2)
    ftp.connect("jing.tk", 21)
    ftp.login("ftpuser", "ftpuser123")
    ftp.cwd("test")
    ftp.dir()
    ftp.quit()
    return ftp


def tls_conn():
    ftp = FTP_TLS(timeout=30)
    ftp.connect("jing.tk", 21)
    ftp.set_pasv(True)
    ftp.auth()
    ftp.prot_p()
    ftp.login("ftpuser", "ftpuser123")
    ftp.cwd("test")
    ftp.dir()


def base_operation():
    ftp = conn()
    ftp.dir()
    ftp.quit()


if __name__ == '__main__':
    # base_operation()
    # conn()
    tls_conn()
