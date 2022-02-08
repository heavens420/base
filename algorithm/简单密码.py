'''
假设渊子原来一个BBS上的密码为zvbo9441987,为了方便记忆，他通过一种算法把这个密码变换成YUANzhi1987，这个密码是他的名字和出生年份，怎么忘都忘不了，而且可以明目张胆地放在显眼的地方而不被别人知道真正的密码。


他是这么变换的，大家都知道手机上的字母： 1--1， abc--2, def--3, ghi--4, jkl--5, mno--6, pqrs--7, tuv--8 wxyz--9, 0--0,就这么简单，渊子把密码中出现的小写字母都变成对应的数字，数字和其他的符号都不做变换，


声明：密码中没有空格，而密码中出现的大写字母则变成小写之后往后移一位，如：X ，先变成小写，再往后移一位，不就是 y 了嘛，简单吧。记住，Z 往后移是 a 哦。

输入：
YUANzhi1987

输出：
zvbo9441987

'''


def convert_lower(ch):
    if 'a' <= ch <= 'c':
        return 2
    elif 'd' <= ch <= 'f':
        return 3
    elif 'g' <= ch <= 'i':
        return 4
    elif 'j' <= ch <= 'l':
        return 5
    elif 'm' <= ch <= 'o':
        return 6
    elif 'p' <= ch <= 's':
        return 7
    elif 't' <= ch <= 'v':
        return 8
    elif 'w' <= ch <= 'z':
        return 9


def convert_upper(ch):
    if ord(ch) == 90:
        return 'a'
    else:
        return chr(ord(ch) + 1).lower()


def simple_passwd():
    value = input()

    value = list(value)
    for i in range(len(value)):
        # 大写字母
        if 65 <= ord(value[i]) <= 90:
            value[i] = str(convert_upper(value[i]))
        elif 97 <= ord(value[i]) <= 122:
            value[i] = str(convert_lower(value[i]))
        else:
            pass

    print("".join(map(str, value)))


if __name__ == '__main__':
    simple_passwd()