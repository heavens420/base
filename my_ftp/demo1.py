from ftplib import FTP

with FTP() as ftp:
    # def ftp_test():
    #     ftp = FTP()
    # 调试信息 默认0 最高2 等级越高打印的日志越多
    ftp.set_debuglevel(2)
    ftp.connect("jing.tk", 21)
    ftp.login("ftpuser", "ftpuser123")
    # print(ftp.welcome+"\n 你好")
    # ftp.cwd(r".")

    # cd
    ftp.cwd(r"test")
    # ls
    files = ftp.nlst()
    # print(files)
    # ll
    # files_ll = ftp.retrlines("LIST")
    # ONLY PRINT FILE NAMES
    # files_ll2 = ftp.retrlines("NLST")
    # files_ll3 = ftp.retrlines("RETR")
    # print(files_ll)
    # ll ,too
    # ftp.dir()

    # 文件下载
    file_path2 = open(r'C:\workspace\python\w1\base\myos\ppp', 'wb')
    remote_path2 = r'/test/Dockerfile'
    buffer_size2 = 1024
    ftp.retrbinary('RETR' + file_path2.write, buffer_size2)
    # file3 = ftp.sendcmd("ls")
    # print(file3)
    # file4 = ftp.voidcmd("ls")

    # 设置被动模式
    # ftp.set_pasv(True)

    # 文件上传
    file_path = open("./demo1.py", "rb")
    remote_path = "/test/111.py"
    buffer_size = 1024 * 10
    ftp.storbinary('STOR ' + remote_path, file_path, buffer_size)
    ftp.set_debuglevel(0)
    # ftp.quit()

# if __name__ == '__main__':
#     ftp_test()
