import pandas as pd

path = r'C:\Users\420\Desktop\动态测试映射模板.xlsx'
data = pd.read_excel(path)

print('---------查看某一列的数据类型------------')
print(data['序号'].dtype)

print('---------------转换数据类型----------------')
print(data['序号'].astype('string'))

print('--------将某列设置为索引列----------------')
print(data.set_index("请求方法"))

print('----------重命名索引---------------')
print(data.rename(index={0: 'q', 1: 'w'}))
print('---------------重命名列名称----------------')
print(data.rename(columns={'序号': '新序号'}))
