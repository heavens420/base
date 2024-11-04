'''

01.2.3.8
1.02.3.8
1.2.03.8
1.2.3.08
0.2.3.8
1.0.3.8
1.2.0.8
1.2.3.0
+1.2.3.8
1.+2.3.8
1.2.+3.8
1.2.3.+8
0.1.2.3.8
1.3.8
.1.3.8
1..3.8
1.3..8
1.3.8.

8.14.139.194
159.97.85.231

120.63.257.146
97.5.217.231

1.02.3.8
1.2.03.8
1.2.3.08


'''


# import re


def ip_judge():
    value = input()
    #
    # expr = r'(\d+\.){3}\d+'
    # reg = re.compile(expr)
    # res = reg.match(value)
    #
    # if not res:
    #     return 'NO'

    # 必须先转成int类型 列表 否则找不出最大最小值
    value = value.split(".")

    if value[-1] == '0':
        return 'NO'

    if len(value) != 4:
        return 'NO'

    for it in value:
        if it.strip() == '':
            return 'NO'
        elif it.startswith("0") and len(it) > 1:
            return 'NO'
        elif int(it) > 255 or int(it) < 0:
            return 'NO'
        elif not it.isdigit():
            return 'NO'
        else:
            pass
    return 'YES'


if __name__ == '__main__':
    while 1:
        try:
            print(ip_judge())
        except Exception as e:
            # print(e)
            break
