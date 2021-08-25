import openpyxl as xl

'''
    just find the differences about two sheets's column
'''

path1 = r''
path2 = r''

wb1 = xl.load_workbook(path1)
wb2 = xl.load_workbook(path2)

sheet1 = wb1.sheetnames
sheet2 = wb2.sheetnames

ws1 = wb1[sheet1[0]]
ws2 = wb1[sheet1[1]]

column1 = ws1['A']
column2 = ws2['B']

def compare(sheet1, sheet2):
    pass
