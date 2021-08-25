import openpyxl as xl
import re

# 被比较者（target）
path = r'C:\Users\420\Desktop\kdgc\6月集团考核\数据网IP专业RES Open API设计-20210525-安徽反馈(1).xlsx'
# 比较者 （sample）
path2 = r'C:\Users\420\Desktop\kdgc\6月集团考核\附件1-集团考核API实指令模版-华为反馈V2版20210622.xlsx'
# 加载target excel
wb = xl.load_workbook(path)
# 加载 sample excel
wb2 = xl.load_workbook(path2)
# 创建新的excel 用来保存比较结果差异
wb3 = xl.Workbook()

# 激活excel
wb.active
wb2.active
ws3 = wb3.active

# 获取excel中所有sheet名称并转化为集合
sheets = wb.sheetnames
sheets2 = wb2.sheetnames

# 决定加载第几个sheet
ws = wb[sheets[1]]
ws2 = wb2[sheets2[0]]

# target列数据 API名称
column_name = ws['B']
# target列数据 API编码
column_code = ws['A']
# target列数据  参数编码
column_para = ws['I']
# 参数类型 出参 入参
para_in_out_type = ws['F']

# sample API编码
code2 = ws2['B']
# sample 实指令内容
cmdtext = ws2['H']

# key为API名称 value为 其对应的所有参数
# target 字典
dicc = dict()
# sample 字典
dicc2 = dict()

'''
    以code为key 参数编码为value 存入字典，为空的code自动取值上一个非空code，这样就实现了 所有编码与其参数的对应关系
'''


def get_code_para1():
    key = ''
    for i in range(len(column_para)):
        temp = column_code[i].value
        if temp is not None:
            # dicc[temp] = column_para[i].value
            key = temp
            print(key)
        if temp is None:
            para_code = column_para[i].value
            # dicc[key] = para_code
            print(key)


# get_code_para1()

'''
    编码为key  参数组成数组为value
'''


def get_code_para():
    key = ''
    lst = set()
    # 遍历target参数列
    for i in range(len(column_para)):
        # 获取target API编码
        temp = column_code[i].value
        # 如果列值为空 即API编码为空
        if temp is not None:
            # if len(lst) > 0:
            # 如果 API编码为空则说明 该列对应的API编码应该是和其上一行(如果上一行为空 就继续上一行 直到非空为止)的值
            dicc[key] = lst
            # print(lst)

            lst = set()
            # 将API编码赋值给key，用于上面获取列值为空的API编码
            key = temp
            # 入参加入列表
            if para_in_out_type[i].value == '入参':
                # 替换target 入参中的 >
                lst.add(str(column_para[i].value).replace('>', ''))
        else:
            # 如果API编码非空 则同样取其入参 组成最终列表
            para_code = column_para[i].value
            if para_in_out_type[i].value == '入参':
                lst.add(str(para_code).replace('>', ''))
    # print(dicc)
    return dicc


get_code_para()

'''
    解析path2中指令内容 将参数提取出来存入列表

    {sd}{dsd}{23}
'''


def get_params(text):
    # text = "folds${dd}${dfs}${ k dsf }"
    # 正则匹配所有参数
    lst = re.findall(r'\${([^}]*)}', text)
    lst2 = set()
    # 遍历所有参数组成的集合
    for i in range(len(lst)):
        # 去除参数两边的空格
        para = lst[i].strip()
        # 如果参数非空加入集合
        if not para.isspace():
            lst2.add(para)
            # print(para)
    # print(lst2)
    # lst2.add('dd')
    return lst2


# ppp = get_params("folds${dd}${dfs}${ k dsf }")
# print(ppp)

'''
    以path2 的指令编码为key  参数集合为value
'''


def path2_key_value():
    # 遍历sample参数列
    for i in range(len(code2)):
        # 获取列值 即参数编码
        key = code2[i].value
        # 获取sample指令内容 并转成字符串
        text = str(cmdtext[i].value)
        # 调用参数取值方法 获取每个API的所有参数
        values = get_params(text)
        # 将参数列表 存入value key为API编码
        dicc2[key] = values
    return dicc2


path2_key_value()

'''
    遍历path和path2 比较key相同的参数是否相同  不同的打印记录
'''


def compare_para():
    # sample总行数
    count_sum = 0
    # 不同的API行数
    count_diff = 0
    # 比较target和sample的API编码
    for c2 in dicc2:
        # sample总数加一  在这里加而不是下面 c1 == c2 里面加的原因是，如果sample中不存在 则行号保留跳过该行
        count_sum += 1
        for c1 in dicc:
            if c2 == c1:
                # # sample总数加一
                # count_sum += 1
                # 要忽略的参数
                ignore = {'deviceId'}
                # 获取target API编码对应的参数
                dic1 = dicc.get(c1) - ignore
                # 获取sample API编码对应的参数
                dic2 = dicc2.get(c2)
                # 取并集
                union = dic2 | dic1
                # 取交集
                jiao = dic1 & dic2
                # 并集和交集的差集 即为二者不同的参数集合
                cha = union - jiao
                # 定义行号 具体加几 跑一下看看就知道了 所有行都往后推 --》 每一行都往后推 所以每行都得加3
                row_num = count_sum + 3
                # 非空说明 存在差异
                if cha != set():
                    # 差异数加一
                    count_diff += 1
                    # 相等说明 参数数量一致但存在参数编码不同
                    if len(dic2) == len(dic1):
                        # print(f'行号:{count_sum + 7},指令编码:{c2},参数名称不同,参数:{cha}')
                        # 加7的目的是为了 和sample中的行号保持一致 方便检查比较 sample中有7个空行
                        ws3.cell(row=row_num, column=1, value=int(row_num))
                        # 将API编码写入第二列
                        ws3.cell(row=row_num, column=2, value=c2)
                        # 参数名称不同 加以说明 写入第三列
                        ws3.cell(row=row_num, column=3, value='参数名称不同')
                        # 记录不同的参数编码 写入第四列
                        ws3.cell(row=row_num, column=4, value=str(cha))
                    else:
                        # print(f'行号:{count_sum + 7},指令编码:{c2},参数数量不同,参数:{str(cha)}')
                        ws3.cell(row=row_num, column=1, value=int(row_num))
                        ws3.cell(row=row_num, column=2, value=c2)
                        ws3.cell(row=row_num, column=3, value='参数数量不同')
                        ws3.cell(row=row_num, column=4, value=str(cha))
                # 差集为空 二者参数一致
                if cha == set():
                    # print(f'行号:{count_sum + 7},指令编码:{c2}')
                    # 直接写行号编码到新的excel
                    ws3.cell(row=row_num, column=1, value=int(row_num))
                    ws3.cell(row=row_num, column=2, value=c2)

    print(f'总计检查{count_sum}条记录，其中{count_diff}条存在差异')
    # 保存新的excel
    wb3.save('result.xlsx')


compare_para()


def test_list():
    lst1 = set([1, 2, 3])
    lst2 = set([4])
    lst3 = lst2 - lst1
    print(lst3)

# test_list()
