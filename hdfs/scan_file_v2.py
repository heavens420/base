from hdfs import InsecureClient
import time
import datetime
import os

'''
    v2: 解决bug: 这bug不好描述，更不好测，而且出现几率非常小，但还是可能会出现。
        概念: 先定义个概念，把每次循环记为一个流程分为两个步骤，第一个步骤就是第一次扫描，获取的文件称之为pre_xxx_list,
             第二个步骤，就是第二次扫描，获取的文件称之为cur_xxx_list
             我们把第一次扫描的文件结果pre_xxx_list称之为基础列表，把第二次扫描的文件列表cur_xxx_list称之为变化列表
             变化列表和基础列表比较，就可以得到变化的文件有那些。
        基于以上概念：
             第二次扫描目录的时候，没有结束扫描的时候，突然在扫过的目录里面新增一个文件，这时候，变化列表肯定不包含这个发生变化的文件
             第二次扫描结束，即意味着一个循环周期的结束
             下一个执行周期，又会重新扫描整个目录得到基础列表，那么，问题出现了，上一周期的第二个步骤中新增的文件将被扫描到当前周期的基础列表中
             但这个变化的文件理应作为下一周期的变化列表的元素，只有这样才能够监控到这个文件的变化，显然如果以上情况发生，则该文件将被遗忘
        解决方案：
             每当一个执行周期(两个步骤)执行结束，就把当前周期的变化列表作为下一周期的基础列表，这样，即便在本周期第二阶段发生文件变化，在下一周期
             的第二阶段也会被重新发现，被遗忘的文件再次被加入记忆
'''
class ScanFile(object):
    def __init__(self, path, expr_time):
        # 用于第一次获取hdfs文件信息集合标志
        self.flag = True
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
        # 获取hdfs所有文件全路径名称集合
        if self.flag:
            # 只有项目启动的时候 获取一次
            self.pre_file_list, self.pre_name_list = self.get_file_list(self.expr_time)
            # 下次是否执行此代码块标志
            self.flag = False
        # 暂停5秒
        time.sleep(5.00)
        # 再一次获取hdfs文件信息集合
        cur_file_list, cur_name_list = self.get_file_list(self.expr_time)

        # 删除的文件集合
        del_file_list = self.pre_name_list - cur_name_list
        # 打印文件监控信息
        print_files(del_file_list, '发现文件删除')

        # 新增的文件集合
        new_file_list = cur_name_list - self.pre_name_list
        # 打印文件监控信息
        print_files(new_file_list, '发现文件新增')

        # 修改的文件集合
        for cur in cur_file_list:
            for pre in self.pre_file_list:
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
    sf = ScanFile('/', 3000)
    while 1:
        try:
            sf.operate()
        except Exception as e:
            print(f'程序出现异常: {e}')
