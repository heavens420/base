'''
    先将7进制转为10进制 计算之后 再将10进制转为7进制
'''

def sum_num(num):
    num = list(num)
    num.reverse()
    po = 0
    sum = 0
    for i in num:
        sum += int(i) * pow(7, po)
        po += 1
    return sum


def sum_7(sum):
    lst = []
    while sum != 0:
        k = sum % 7
        sum //= 7
        lst.append(k)
    return lst


if __name__ == '__main__':
    while 1:
        a, b = input().split()
        sum = sum_num(a) + sum_num(b)
        # print(sum)
        res = sum_7(sum)
        res.reverse()
        print("".join(map(str,res)))
