'''

输入一个只包含个位数字的简单四则运算表达式字符串，计算该表达式的值
注：
3.1、表达式只含 +, -, *, / 四则运算符，不含括号
3.2、表达式数值只包含个位整数(0-9)，且不会出现0作为除数的情况
3.3、要考虑加减乘除按通常四则运算规定的计算优先级
3.4、除法用整数除法，即仅保留除法运算结果的整数部分。比如8/3=2。输入表达式保证无0作为除数情况发生
3.5、输入字符串一定是符合题意合法的表达式，其中只包括数字字符和四则运算符字符，除此之外不含其它任何字符，不会出现计算溢出情况


示例:
1）输入：char *expStr = “3*2-5*2+8”
函数返回：4


思路:
    将所有字符存入数组，根据优先级，先处理 * / ，根据 * / 获取其前后的数字运算 然后修改参与运算的三个符号位 使其不再参与后面的运算 最后将所有运算结果相加，即为结果
'''


# 10+20-40+2*2+3*1-3/2+4/2

def calculate():
    expr = input()

    num = []
    for i in range(len(expr)):
        num.append(expr[i])

    # 优先计算乘除法
    for it in range(len(num)):
        if num[it] == '*':
            sum = int(num[it - 1]) * int(num[it + 1])
            # it+1索引赋值而不能其它两个参与运算的索引赋值 因为乘除法可能是连续的 赋值给最后一个参与运算的索引 便于多级乘除法连续计算
            num[it + 1] = sum
            # 参与运算之后 加标记 不要重复再计算
            num[it - 1] = None
            num[it] = None

        if num[it] == '/':
            sum = int(num[it - 1]) // int(num[it + 1])
            num[it + 1] = sum
            num[it - 1] = None
            num[it] = None

    result_num = []
    # 这里要先过滤掉 None值 因为 可能出现 - 前后都是None值 无法确定下一个要减去的数的位置 去None值后 - 后面就一定是一个要参与计算的数字
    for ite in range(len(num)):
        if num[ite] is not None:
            result_num.append(num[ite])

    result = 0
    # 对最终列表累加计算，遇到 - 号的 后一位直接取反 当前位直接置零以不影响当前运算结果
    for item in range(len(result_num)):
        if result_num[item] is not None and result_num[item] != '+':
            if result_num[item] == '-':
                result_num[item + 1] = -int(result_num[item + 1])
                result_num[item] = 0
            result += int(result_num[item])
    print(result)


if __name__ == '__main__':
    calculate()
    # a = 1 + 2 * 3 // 4
    # print(a)
