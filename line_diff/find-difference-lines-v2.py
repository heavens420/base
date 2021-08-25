import re

from line_diff.format_xml import execute_format

'''
    find difference about two file's lines with no-ordered
'''

# 格式化xml文件，并将格式化后的文件写入新文件
execute_format()


# 过滤规则: 过滤含有中文的整行，过滤xml标签内容为空的，去除空格换行符等特殊字符
def filter_chinese(str):
    regex = r'.*[\u4e00-\u9fa5].*|\n|\s'
    # match = re.compile(regex)
    result = re.sub(regex, '', str)
    # result = match.findall(str)
    return result
    # print(result)


# files = open(r'/line_diff/激活-format.xml', 'r', encoding='utf-8')

# filter_chinese(files.read(500))

# 读取要比对的两个文件
with open(r'C:\workspace\python\w1\base\line_diff\激活-format.xml', 'r', encoding='utf-8') as file, \
        open(r'C:\workspace\python\w1\base\line_diff\采控-format.xml', 'r', encoding='utf-8') as file2:
    # print(file)
    # 逐行读取，每一行都是集合中的一个元素，按照正则规范对集合元素进行更改
    lst = set(map(filter_chinese, file.readlines()))
    lst2 = set(map(filter_chinese, file2.readlines()))

    # 激活 - 采控
    cha1 = lst - lst2
    # 采控 - 激活
    cha2 = lst2 - lst

    cha3 = cha1 | cha2

    print(f'激活比采控多:{cha1}')
    print(f'采控比激活多:{cha2}')
    print(f'差异汇总:{cha3}')
