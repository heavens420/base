"""
    俩文件  字段连接  输出结果
"""

'''
    'r'：读
    'w'：写
    'a'：追加
    'r+' == r+w（可读可写，文件若不存在就报错(IOError)）
    'w+' == w+r（可读可写，文件若不存在就创建）
    'a+' ==a+r（可追加可写，文件若不存在就创建）
    对应的，如果是二进制文件，就都加一个b就好啦：
    'rb'　　'wb'　　'ab'　　'rb+'　　'wb+'　　'ab+'
'''


class FileJoin:
    def __init__(self, target_path, another_path, another_column_num):
        # 仅此一份的文件列表
        self.target_file_list = list()
        # 其它n个文件列表
        self.another_file_list = list()
        #
        self.target_path = target_path
        self.another_path = another_path
        # 要比较的列序号 从1开始
        self.another_column_num = another_column_num

    # 处理行 将每个字段作为一个元素 每行(hang)行(xing)成一个列表
    def split_column(self, file_path):
        new_file_list = list()
        file_list = self.get_file_list(file_path)
        for line in file_list:
            line_list = str(line).split('|^|')
            new_file_list.append(line_list)
        return new_file_list

    # 按行读取文件 每行作为一个元素 形成列表
    def get_file_list(self, file_path):
        with open(file_path, 'r', encoding='gbk') as file:
            return file.readlines()

    # 生成对比文件的行列表 即以行的列值为元素的 二维列表
    def get_target_file_list(self):
        self.target_file_list = self.split_column(self.target_path)

    # 同上
    def get_another_file_list(self):
        self.another_file_list = self.split_column(self.another_path)

    # 恢复原文件格式 自动写入文件
    def recovery_file_style(self, line_list):
        with open('result.txt', 'a+') as file:
            for column in line_list:
                text = ''
                if column == '\n' or column == '':
                    text = column
                else:
                    text = column + r'|^|'
                file.write(text)

    # 两个表的连接操作 指定列ID相同的行 将被筛选出来
    def join_by_id(self):
        self.get_target_file_list()
        self.get_another_file_list()

        for target in self.target_file_list:
            for another in self.another_file_list:
                if str(target[0]).strip() == str(another[self.another_column_num - 1]):
                    self.recovery_file_style(another)
                    print(another)


'''
    如何使用：修改两个文件路径 打开cmd 输入 python join_id.py 控制台将打印比对结果 同时在执行目录下生成结果文件
'''

if __name__ == '__main__':
    # 其它文件都要和这个独一份的文件比对
    # param1 : 独一份的文件
    # param2 : 其它要比较的文件
    # param3 : 其它文件要用哪一列和独一份文件的ID比较，第一列即1 第n列即为n
    param1 = r'C:\Users\420\Desktop\资源数样例文件\V_ACCESS_DEV_szx_20210511.txt'
    param2 = r'C:\Users\420\Desktop\new 7.txt'
    param3 = 4

    fj = FileJoin(param1, param2, param3)
    fj.join_by_id()
