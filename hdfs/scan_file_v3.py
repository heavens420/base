from hdfs import InsecureClient
import time
import datetime
import os

'''
    v3: 优化代码结构 嗯对 仅此而已
'''


class ScanFile(object):
    def __init__(self, path, expr_time):
        # 相对当前时间而言的前一次文件信息列表
        self.pre_file_list = []
        # 相对当前而言的前一次文件名称全路径集合
        self.pre_name_list = set()
        # hdfs路径
        self.path = path
        # 文件过期时间(单位秒)
        self.expr_time = expr_time
        # hdfs地址
        self.url = 'http://192.168.80.220:50070'
        # hdfs用户
        self.user = 'hadoop'
        # 创建hdfs连接
        self.client = InsecureClient(url=self.url, user=self.user)

    def operate(self):
        # 获取当前hdfs文件信息集合
        cur_file_list, cur_name_list = self.get_file_list(self.expr_time)

        # 相等时 说明集合和列表为空 否则不可能相等 为空说明是第一次执行 则不需要执行具体操作
        # if self.pre_file_list != list(self.pre_name_list): 经本地测试，1kw长度的集合此行代码耗时0.01秒 1w长度的集合耗时0 下面写法耗时0
        if self.pre_file_list != list() and self.pre_name_list != set():
            # 删除的文件集合
            del_file_list = self.pre_name_list - cur_name_list
            # 打印文件监控信息
            print_files(del_file_list, '发现文件删除')

            # 新增的文件集合
            new_file_list = cur_name_list - self.pre_name_list
            # 打印文件监控信息
            print_files(new_file_list, '发现文件新增')

            # 修改的文件集合
            for pre in cur_file_list:
                for cur in self.pre_file_list:
                    # 文件名称相同
                    if cur['absolutePath'] == pre['absolutePath']:
                        # 修改时间不同
                        if cur['modificationTime'] != pre['modificationTime']:
                            # 说明文件被修改过 打印监控信息
                            print(f'{datetime.datetime.now()} 发现文件修改 {cur["absolutePath"]}')

        # 将当前文件信息列表赋值给前一次文件信息列表
        self.pre_file_list, self.pre_name_list = cur_file_list, cur_name_list

    # 创建hdfs文件信息集合
    def get_file_list(self, expr_time):
        file_list = list()
        name_list = set()
        # 遍历整个hdfs文件目录
        for root, dirs, files in self.client.walk(self.path, status=True):
            # 遍历某个目录下文件的所有文件
            for item in files:
                # 文件信息非空 即文件存在
                if item != tuple():
                    # 获取文件的全路径名称，用以区分不同目录的同名文件
                    full_path = os.path.join(root[0], item[0])
                    # 扩增文件status信息
                    item[1]['absolutePath'] = full_path
                    # 将文件包括其文件信息加入文件列表
                    file_list.append(item[1])
                    # 只将文件全路径加入列表 用以快速判断文件新增和删除
                    name_list.add(full_path)

                    # 判断文件是否过期
                    # 获取当前时间秒
                    now = time.time()
                    # 如果文件最后一次的编辑时间 + 文件允许的存在时间 < 当前时间  则说明 文件过期 需要删除
                    if item[1]['modificationTime'] / 1000.0 + expr_time < now:
                        # 是否删除成功 boolean类型
                        success = self.client.delete(hdfs_path=full_path)
                        # 打印语句内容
                        result = "删除成功" if success else "删除失败"
                        print(f'{datetime.datetime.now()} 发现文件过期,{result} {full_path}')
        return file_list, name_list


# 打印监控信息方法
def print_files(list_files, operation):
    for file in list_files:
        # 打印信息内容: 当前时间 文件状态 文件全路径
        print(f'{datetime.datetime.now()} {operation} {file}')


if __name__ == '__main__':
    # 参数: hdfs扫描路径，文件保存时间(单位秒)
    sf = ScanFile('/', 300000)
    while 1:
        try:
            sf.operate()
            time.sleep(5.000000)
        except Exception as e:
            print(f'程序出现异常: {e}')
