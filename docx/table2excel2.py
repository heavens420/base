from docx import Document
import openpyxl as xl


# excel_path = r'C:\Users\420\Desktop\調研轉換結果.xlsx'
pre_path = "C:\\Users\\420\\Desktop\\kdgc\\new2\\"
suffix_path = "陕西反馈"
xlsx = ".xlsx"

excel_path = pre_path+suffix_path+xlsx
# sheet_name = '吉林111'
# index = 3

# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\2021-03-02 IDC数通设备调研表V2-海南.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\2021-IDC数据设备调研表-黑龙江.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表(吉林).docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表(天津).docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表(山东).docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表(河南).docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-云南20210304.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-内蒙园区.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-四川IDC.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-宁夏.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-安徽.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-广东.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-广西公司汇总.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-广西公司汇总v2.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-新疆.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-浙江.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-湖北.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-甘肃.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-贵州园区.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-辽宁2021.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-重庆.docx'
word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-陕西反馈.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表-青海.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表0304v2.1-福建.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表0305-河北.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表1-江苏.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表——山西.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表——西藏.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\iDC数通设备调研表（海南）.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研表（贵州）.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\北京IDC数通设备调研表.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研-内蒙IDC\IDC数通设备调研表-乌兰察布【虚拟IDC】.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研-内蒙IDC\IDC数通设备调研表-乌海【虚拟IDC】.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研-内蒙IDC\IDC数通设备调研表-包头【虚拟IDC】.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研-内蒙IDC\IDC数通设备调研表-呼和浩特【虚拟IDC】.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研-内蒙IDC\IDC数通设备调研表-呼和浩特（云计算园区）.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研-内蒙IDC\IDC数通设备调研表-巴盟【虚拟IDC】.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研-内蒙IDC\IDC数通设备调研表-赤峰【虚拟IDC】.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研-内蒙IDC\IDC数通设备调研表-鄂尔多斯【虚拟IDC】.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研-内蒙IDC\IDC数通设备调研表-鄂尔多斯（云计算园区）.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\IDC数通设备调研-内蒙IDC\IDC数通设备调研表（内蒙）.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\上饶-IDC数通设备调研表-上饶.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\九江-IDC数通设备调研表(1).docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\南昌-IDC数通设备调研表(1)-南昌反馈.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\吉安-IDC数通设备调研表(吉安反馈).docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\宜春-IDC数通设备调研表(1).docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\抚州-IDC数通设备调研表(抚州).docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\新余-IDC数通设备调研表-新余.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\景德镇-IDC数通设备调研表.docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\省中心-IDC数通设备调研表(1).docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\萍乡-IDC数通设备调研表(1).docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\赣州-IDC数通设备调研表(赣州).docx'
# word_path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式\江西-IDC数通设备调研表\鹰潭-IDC数通设备调研表-鹰潭.docx'


obj = Document(word_path)
wb = xl.Workbook()
# wb = xl.load_workbook(excel_path)
# wb.create_sheet(sheet_name, index)
ws = wb.active

tables = obj.tables

lst = list()
file_lst = list()
row_num = 1
col = 1

title_lst = ['省份', '类型', '地市', '设备名称', '设备厂家', '设备型号', '所在IDC及AS', '设备版本', '设备IP', 'LOOPBACK', '设备数量', '物理服务器还是虚拟主机',
             '物理设备型号配置/或虚拟机配置简况', '系统版本', '备注']


def get_title():
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


def foreach_all_tables():
    get_title()
    global row_num
    for k in range(1, 7):
        table1 = tables[k]
        title_item = lst[k - 1]
        for i in range(1, len(table1.rows)):
            row_num = row_num + 1
            count = 3
            for j in range(0, len(table1.columns)):
                content1 = table1.cell(i, j).text
                title2 = table1.cell(0, j).text
                if count == len(table1.columns) - 1:
                    row_num -= 1
                if content1 is None or content1 == '无其他设备' or content1 == '无其他设备' == '无' or str(content1).strip() == '':
                    count += 1
                    continue
                device_type(title_item, ws, title2, content1, row_num)
    print(f'总行数:{row_num}')


foreach_all_tables()
wb.save(excel_path)
