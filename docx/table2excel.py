from docx import Document
import openpyxl as xl
import os
import threading
import time

# word_path = r'C:\Users\420\Desktop\IDC数通设备调研表-安徽.docx'
dir_path = r'C:\Users\420\Desktop\kdgc\new'
word_path = r'C:\Users\420\Documents\WeChat Files\wxid_d6s6ieyj6kyd12\FileStorage\File\2021-08\各省数通联系方式\IDC数通设备调研表-云南20210304.docx'
excel_path = r'C:\Users\420\Desktop\調研轉換結果.xlsx'
# obj = Document(word_path)
wb = xl.Workbook()
ws = wb.active

# tables = obj.tables

lst = list()
file_lst = list()
row_num = 1
col = 1
lock = threading.Lock

title_lst = ['省份', '类型', '地市', '设备名称', '设备厂家', '设备型号', '所在IDC及AS', '设备版本', '设备IP', 'LOOPBACK', '设备数量', '物理服务器还是虚拟主机',
             '物理设备型号配置/或虚拟机配置简况', '系统版本', '备注']


def get_all_file_names(dir_path):
    for root, dirs, files in os.walk(dir_path):
        # print(files, end='\n')
        # print(type(files))
        for fi in files:
            file_lst.append(fi)


print(file_lst)


def foreach_dir():
    print("dddddddddd")
    for file_name in file_lst:
        print(file_name, end="\n")
        base_path = 'C:\\Users\\420\\Desktop\\kdgc\\new\\'
        file_path = base_path + file_name
        obj = Document(file_path)
        get_title(obj)
        tables = obj.tables
        # time.sleep(30)
        excel_path = "C:\\Users\\420\\Desktop\\kdgc\\new2\\" + str(file_name) + ".xlsx"
        foreach_all_tables(tables, row_num, excel_path)
        # wb.save(excel_path)


def get_title(obj):
    for txt in obj.paragraphs:
        title = txt.style.name
        if str(title).startswith("Heading 3"):
            content = str(txt.text)
            if content.__contains__('IDC-') and not content.__contains__('）情况：'):
                # print(content)
                lst.append(content)


for item in title_lst:
    ws.cell(row=1, column=col, value=item)
    col += 1


# 填充行
def name2name(ws1, tit, con, row_num):
    for i in range(len(title_lst)):
        if title_lst[i] == tit:
            con = str(con).strip()
            ws1.cell(row=row_num, column=i + 1, value=con)


def device_type(type, ws, title2, content1, row_num):
    if type.__contains__('设备列表'):
        # 路由器
        ws.cell(row=row_num, column=2, value='路由器')
    if type.__contains__('防火墙'):
        # 防火墙
        ws.cell(row=row_num, column=2, value='防火墙')
    if type.__contains__('交换机'):
        # 交换机
        ws.cell(row=row_num, column=2, value='交换机')
    if type.__contains__('质量测试服务器'):
        # 质量测试服务器
        ws.cell(row=row_num, column=2, value='质量测试服务器')
    if type.__contains__('其它'):
        # 其它
        ws.cell(row=row_num, column=2, value='其它')
    name2name(ws, title2, content1, row_num)


def foreach_all_tables(tables, row_num, excel_path):
    for k in range(1, 7):
        table1 = tables[k]
        title_item = lst[k - 1]
        for i in range(1, len(table1.rows)):
            row_num = row_num + 1
            for j in range(0, len(table1.columns)):
                content1 = table1.cell(i, j).text
                title2 = table1.cell(0, j).text
                if content1 is None or content1 == '无其他设备' or str(content1).strip() == '':
                    # row_num -= 1
                    break
                device_type(title_item, ws, title2, content1, row_num)
    print(f'总行数:{row_num}')
    wb.save(excel_path)


# def del_blank_row():

# foreach_all_tables(row_num)
get_all_file_names(dir_path)
foreach_dir()
# wb.save(excel_path)
