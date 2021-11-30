import paramiko


def create_ssh_key():
    host = "jing.tk"
    port = 65535
    username = "root"
    passwd = "you know ? you don't know !"
    # 配置私人密钥文件位置
    # private = paramiko.RSAKey.from_private_key_file(r'C:\Users\420\.ssh\heavens')
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(hostname=host, port=port, username=username, password=passwd)
    # ssh_client.connect(hostname=host, port=port, username=username, pkey=private)
    stdin, stdout, stderr = ssh_client.exec_command('ps -aux')
    print(stdin)
    print(stdout)
    print(stderr)
    ssh_client.close()


def conn():
    host = "jing.tk"
    port = 65535
    username = "root"
    private = paramiko.RSAKey.from_private_key_file(r'C:\Users\420\.ssh\heavens')
    host_port = (host, port)
    transport = paramiko.Transport(host_port)
    transport.connect(username=username, pkey=private)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp, transport
    # sftp.chdir("/usr/local")
    # dir = sftp.listdir()
    # print(dir)
    # sftp.close()
    # transport.close()


def upload_file():
    sftp, transport = conn()
    local_file = r'demo1.py'
    remote_file = f"/usr/local/src/{local_file}"
    sftp.put(local_file, remote_file)
    sftp.close()
    transport.close()


def download_file():
    sftp, transport = conn()
    remote_file = r'/usr/local/src/kkk.py'
    local_file = r'./ppp.py'
    sftp.get(remote_file, local_file)
    sftp.close()
    transport.close()


if __name__ == '__main__':
    # create_ssh_key()
    # conn()
    # upload_file()
    download_file()
