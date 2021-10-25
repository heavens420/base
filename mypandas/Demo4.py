import pandas as pd

path = r'C:\Users\420\Desktop\动态测试映射模板.xlsx'
data = pd.read_excel(path)

print('--------获取单元格是否为空-----------')
print(data.isnull())

print('-------------删除单元格为空的行-----------')
print(data.dropna())

print('--------删除单元格全为空的行-----------')
print(data.dropna(how='all'))

print('----------------用0填充为空的单元格--------------------')
print(data.fillna(0))

print('-------------删除重复的行------keep:表示保存哪一行----可选参数---first--last--false:代表全删除-------------')
print(data.drop_duplicates(subset="测试入参(json)", keep='last'))
print('-----------根据多个字段判断是否删除-------------')
print(data.drop_duplicates(subset=['标准API名称', '请求方法']))

