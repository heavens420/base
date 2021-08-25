import re

'''
    find difference about two file's lines with no-ordered
'''

# 过滤规则: 过滤含有中文的整行，过滤xml标签内容为空的，去除空格换行符等特殊字符
def filter_chinese(str):
    regex = r'.*[\u4e00-\u9fa5].*|\n|\s'
    # match = re.compile(regex)
    result = re.sub(regex, '', str)
    # result = match.findall(str)
    return result
    # print(result)


# files = open(r'C:\workspace\python\w1\base\base\io_test-1.txt', 'r', encoding='utf-8')
#
# filter_chinese(files.read(500))

# 读取要比对的两个文件
with open(r'C:\workspace\python\w1\base\line_diff\io_test-1.txt', 'r', encoding='utf-8') as file, \
        open(r'C:\workspace\python\w1\base\line_diff\io_test-2.txt', 'r', encoding='utf-8') as file2:

    # print(file)
    # 逐行读取，每一行都是集合中的一个元素，按照正则规范对集合元素进行更改
    lst = set(map(filter_chinese, file.readlines()))
    lst2 = set(map(filter_chinese, file2.readlines()))

    # 取并集
    bing = lst | lst2
    # 取交集
    jiao = lst & lst2

    # 取差集
    cha = bing - jiao

    # 差集即为 不同的元素，为空说明两个文件相同
    print(cha)
