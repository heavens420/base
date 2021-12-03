import re

ss = "nihaoa zheshijie" \
     "nidemingzi"


def test1():
    reg = r'ni'
    # 从开头开始匹配 开头能匹配的上返回匹配结果 开头第一个字符就匹配不上 报错
    result = re.match(reg, ss)
    print(result.group())
    # 只要包含匹配内容就将结果返回 只返回第一个匹配成功的
    result = re.search(reg, ss)
    print(result.group())
    # 将所有匹配的装进列表返回
    result = re.findall(reg, ss)
    print(result)


def test3():
    reg = r'\w+(i)(\w+)'
    result = re.findall(reg, ss)
    print(result)
    result = re.match(reg, ss)
    i = 0
    while result is not None:
        print(result.group(i))
        i += 1



def test2():
    reg = r'jie'
    regx = re.compile(reg)
    result = regx.search(ss)
    print(result.group())


def test4():
    x = 3
    import datetime
    dt0 = datetime.datetime.strptime('20211101000000', '%Y%m%d%H%M%S')
    dt1 = datetime.datetime.strptime('20211128161347', '%Y%m%d%H%M%S')
    delta = datetime.timedelta(days=(dt1 - dt0).days % x)
    dt2 = dt1 - delta
    print(dt2.strftime('%Y%m%d000000'))


if __name__ == '__main__':
    # test1()
    test3()
    # test4()
