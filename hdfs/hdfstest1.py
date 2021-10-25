from hdfs.client import Client
from hdfs import InsecureClient
import time
import os
import sys
import platform

# url : http://hadoop_address:50070 (端口默認為 http訪問端口) user : 用戶名，錯誤的用戶名不影響讀文件 但是寫文件會報權限不足異常
# client = Client('http://jing.tk:50020', 'user1')
# client = InsecureClient('http://jing.tk:50020', 'root')
# client = InsecureClient('http://192.168.123.205:50070', 'root')
client = InsecureClient('http://192.168.80.220:50070', 'hadoop')

# 列出对应url下的文件夾（不递归）
file = client.list('/test2/file2', status=True)
print(file)

# 获取路径具体信息
# status = client.status('/user/root', strict=False)
# print(status)
# for key in status:
#     print(f'{key}---{status[key]}')
# time.sleep(100)


# 创建文件 (可递归创建) 可加第二个权限参数 makedirs('/root',permission = 777)
# client.makedirs('/test1/file')
# client.makedirs('/test1/file2/file3')

# 写文件
client.write(hdfs_path='/test2/file2/aa.txt', overwrite=True, data='人生苦短，远离python!'.encode('utf-8'))

# client.upload(hdfs_path=r'/test1/file2/file3', local_path=r'C:\Users\420\Downloads\Documents')

# 读文件
# with client.read(hdfs_path=r'/user/root/input/file1.txt', encoding='utf-8') as reader:
#     print(reader.read())

# 递归删除文件 成功返回True 失败返回False
# client.delete(hdfs_path=r'/test1/file2', recursive=True)

# client.download('/user/root/input/file1.txt', r'C:\Users\420\Desktop')

# client.rename('/test1/file-cp', '/test1/file')

# checksum = client.checksum(hdfs_path='/user/root/input/file1.txt')
# print(checksum)

sys.platform = 'linux'

while False:
    file_status = list()
    for root, dirs, file in client.walk('/', status=True):
        print(f'root->{root}')
        print(f'dirs->{dirs}')
        print(f'file->{file}')
        if file != list():
            # print(f'file->{file[0]}')
            # print(f'file-->{type(file)}')  list
            # print(len(file))
            for item in file:
                # tuple
                # print(f'item ==> {type(item)}')
                # item[0]: str
                # item[1]: dict
                # print(f'item[0] --> {item[0]}')
                # print(f'item[1] --> type[item1] --> {type(item[1])} --> {item[1]}')
                # print(f'item[1] --> type[item1] --> {type(item[1])} --> {item[1]["accessTime"]}')
                # print(os.path.join(root[0], item[0]))
                # print(root[0]+'/'+item[0])
                # file_status.append(item[1]["accessTime"])
                # file_status.append(item[1]["modificationTime"])
                # file_status.append(item[1]["pathSuffix"])
                file_status.append(item[1])
                # for tt in item:
                #     print(f'tt-->{type(tt)}')
                #     print(f'item --> {item[1]}')
    # print(file_status)
    time.sleep(5)

print(platform.platform())


def testWalk():
    pre_file_list, pre_name_list = get_file_list()
    time.sleep(5.00)
    cur_file_list, cur_name_list = get_file_list()

    # 删除的
    del_file_list = pre_name_list - cur_name_list
    print_files(del_file_list, '发现文件删除')

    # 新增的
    new_file_list = cur_name_list - pre_name_list
    print_files(new_file_list, '发现文件新增')

    # 修改的
    for cur in cur_file_list:
        for pre in pre_file_list:
            # 文件名称相同
            if cur['absolutePath'] == pre['absolutePath']:
                # 修改时间不同
                if cur['modificationTime'] != pre['modificationTime']:
                    # 说明文件被修改过
                    print(f'{time.time()} 发现文件修改 {cur["absolutePath"]}')

    # pre_file_list, cur_file_list = cur_file_list, list()
    # time.sleep(5.00)


run_flag = True


def get_first_file_list():
    global run_flag
    file_list = list()
    name_list = set()
    if run_flag:
        for root, dirs, files in client.walk('/', status=True):
            for item in files:
                if item != tuple():
                    full_path = os.path.join(root[0], item[0])
                    item[1]['absolutePath'] = full_path
                    file_list.append(item[1])
                    name_list.add(full_path)
        run_flag = False
        # time.sleep(5)
        return file_list, name_list
    else:
        return list(), list()


def get_file_list(expr_time):
    # global file_list1
    file_list1 = list()
    name_list = set()
    for root, dirs, files in client.walk('/', status=True):
        for item in files:
            if item != tuple():
                full_path = os.path.join(root[0], item[0])
                item[1]['absolutePath'] = full_path
                file_list1.append(item[1])
                name_list.add(full_path)

                # 判断文件是否过期
                if item[1]['modificationTime'] / 1000.0 + expr_time > time.time():
                    client.delete(hdfs_path=full_path)
                    print(f'{datetime.datetime.now()} 发现文件过期，进行删除 {full_path}')

    return file_list1, name_list


def print_files(list, operation):
    for file in list:
        print(f'{time.time()} {operation} {file}')


# testWalk()

# client.delete('/test1/file2/aa.txt')


