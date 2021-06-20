import openpyxl as xl
import re

path = r'C:\Users\420\Desktop\kdgc\6月集团考核\数据网IP专业RES Open API设计-20210525-安徽反馈(1).xlsx'
path2 = r'C:\Users\420\Desktop\kdgc\6月集团考核\附件1-集团考核API实指令模版-华为反馈V2版20210611.xlsx'

wb = xl.load_workbook(path)
wb2 = xl.load_workbook(path2)

wb.active
wb2.active

sheets = wb.sheetnames
sheets2 = wb2.sheetnames

ws = wb[sheets[1]]
ws2 = wb2[sheets2[0]]

# column_name = ws['A1': 'B3']
column_name = ws['B']
column_code = ws['A']
column_para = ws['I']
para_in_out_type = ws['F']

code2 = ws2['B']
cmdtext = ws2['H']

dic = dict()
dicc = dict()
dicc2 = dict()

# for i in range(len(column_name)):
#     # print(column_name[i].value, end='\t')
#     dic[column_code[i].value] = column_name[i].value

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
    for i in range(len(column_para)):
        temp = column_code[i].value
        if temp is not None:
            # if len(lst) > 0:
            dicc[key] = lst
            # print(lst)

            lst = set()
            key = temp
            if para_in_out_type[i].value == '入参':
                lst.add(column_para[i].value)
        else:
            para_code = column_para[i].value
            if para_in_out_type[i].value == '入参':
                lst.add(para_code)
    # print(dicc)
    return dicc


get_code_para()

'''
    解析path2中指令内容 将参数提取出来存入列表

    {sd}{dsd}{23}
'''


def get_params(text):
    # text = "folds${dd}${dfs}${ k dsf }"
    lst = re.findall(r'\${([^}]*)}', text)
    lst2 = set()
    for i in range(len(lst)):
        para = lst[i].strip()
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
    for i in range(len(code2)):
        key = code2[i].value
        text = str(cmdtext[i].value)
        values = get_params(text)
        dicc2[key] = values
    return dicc2


path2_key_value()

'''
    遍历path和path2 比较key相同的参数是否相同  不同的打印记录
'''


def compare_para():
    count_sum = 0
    count_diff = 0
    for c2 in dicc2:
        for c1 in dicc:
            if c2 == c1:
                count_sum += 1
                ignore = {'deviceId'}
                dic1 = dicc.get(c1)
                dic2 = dicc2.get(c2)
                union = dic2 | dic1
                jiao = dic1 & dic2
                cha = union - jiao - ignore

                if cha != set() and dic2 != set():
                    count_diff += 1
                    print(f'行号:{count_sum+7},指令编码:{c2},参数:{cha}')

    print(f'总计检查{count_sum}条记录，其中{count_diff}条存在差异')


compare_para()


def test_list():
    lst1 = set([1, 2, 3])
    lst2 = set([4])
    lst3 = lst2 - lst1
    print(lst3)

# test_list()
