import openpyxl as xl

ta_path = r'C:\Users\420\Desktop\kdgc\6月集团考核\附件1-集团考核API实指令模版-华为反馈V2版20210622.xlsx'
wb = xl.load_workbook(ta_path)

wb3 = xl.Workbook()
ws3 = wb3.active

sheet_names = wb.sheetnames
# 加载sample数据
ws = wb[sheet_names[3]]

sa_code = ws['A']
sa_cmd = ws['F']
sa_ser = ws['H']
sa_wrong = ws['I']
sa_params = ws['J']

# 加载target数据 集团API
ws2 = wb[sheet_names[2]]
ta_code = ws2['B']
ta_name = ws2['C']

sa_dict = dict()
ta_dict = dict()

for i in range(len(sa_code)):
    lst = list()

    code = sa_code[i].value
    cmd = sa_cmd[i].value
    ser = sa_ser[i].value
    wrong = sa_wrong[i].value
    params = sa_params[i].value
    lst.append(cmd)
    lst.append(ser)
    lst.append(wrong)
    lst.append(params)
    sa_dict[code] = lst

for j in range(len(ta_code)):
    ta_co = ta_code[j].value
    ta_na = ta_name[j].value
    ws3.cell(row=j + 1, column=1, value=ta_co)
    ws3.cell(row=j + 1, column=2, value=ta_na)

    if ta_co in sa_dict.keys():
        value = sa_dict.get(ta_co)
        for it in range(len(value)):
            cmd = value[0]
            ser = value[1]
            wrong = value[2]
            params = value[3]

            ws3.cell(row=j + 1, column=4, value=cmd)
            ws3.cell(row=j + 1, column=5, value=ser)
            ws3.cell(row=j + 1, column=6, value=wrong)
            ws3.cell(row=j + 1, column=7, value=params)
    else:
        ws3.cell(row=j + 1, column=1, value=ta_co)
        ws3.cell(row=j + 1, column=2, value=ta_na)
        ws3.cell(row=j + 1, column=6, value='反馈的API中不存在')

wb3.save('new_api——2.xlsx')
