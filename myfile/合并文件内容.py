import os


class Merge(object):
    def __init__(self):
        # 源代码路径
        self.input_path = r"C:\workspace\java\w2\yshopmall"
        # 合并后输出代码路径
        self.output_path = r'C:\Users\420\Desktop\事件处理平台数据库\codes\codes.txt'
        # 合并后的代码列表
        self.file_lines = []

    # 读文件
    def read_file(self, file_name):
        # 逐个打开文件读取内容
        with open(file_name, 'r', encoding="utf-8") as file:
            print(f'开始读{file_name}')
            # 获取每一个文件的所有内容 内容和代码原格式相同
            line: str = file.read()
            # 去除空行 如果想保留和源代码相同格式可注释掉本行
            line = line.replace("\n\n", "\n")
            # 将读取的文件内容存入列表
            self.file_lines.append(line)
            # print(f'------> {line}')

    # 写文件
    def write_file(self):
        # 先遍历源代码路径下的所有文件 将文件内容存入合并文件列表
        self.iterator_files()
        # 遍历存有所有文件内容的集合
        for line in self.file_lines:
            # 打开合并代码输出文件
            with open(self.output_path, 'a+', encoding='utf-8') as out:
                # 将合并集合内容写入目标合并文件
                out.write(line)

    # 遍历源代码路径下的所有文件
    def iterator_files(self):
        for root, dirs, files in os.walk(self.input_path):
            # 遍历每一个目录下的所有文件
            for file in files:
                # current_file_path = os.path.join(root, file)
                # 筛选Java文件 只读取java文件内容 其它文件不读
                # 如果想读取其它文件 修改这里的条件
                if str(file).endswith(".java"):
                    # 改变文件目录 cd到当前读取的文件路径
                    os.chdir(root)
                    print(f"当前路径为:{os.getcwd()}")
                    # 开始获取当前文件的内容
                    self.read_file(file)


if __name__ == '__main__':
    m = Merge()
    m.write_file()
