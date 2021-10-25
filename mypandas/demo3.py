import pandas as pd

path = r'C:\Users\420\Desktop\动态测试映射模板.xlsx'
# 根据名称读取sheet
# data = pd.read_excel(path, sheet_name='Sheet1')
# 读取第一个sheet
# data = pd.read_excel(path, sheet_name=0)
# 指定行索引 0代表将第一列的值作为行索引 1代表第二列  索引列将被移至第一列
# data = pd.read_excel(path, sheet_name=0, index_col=1)

# 只导入特定的列
# data = pd.read_excel(path, sheet_name=0, index_col=0, usecols=[0, 5])


print('-------------读取csv--------------')
path2 = r''
# 默认以逗号作为分隔符，可指定分隔符 如空格分隔
# data = pd.read_csv(path2, sep=' ')
# 只读取两行
# data = pd.read_csv(path2, sep=' ', nrows=2)
# 指定编码
# data = pd.read_csv(path2, sep=' ', nrows=2, encoding='utf-8')


print('----------读取txt文件-----------')
path3 = r'C:\Users\420\Desktop\demo1.py'
# 读取txt文件 并指定分隔符 也可以读取csv文件
data = pd.read_table(path3, sep=' ')
print(data)
print(type(data))

print('-----------------数据属性----------------')
# 只读取5行
print(data.head(5))
# 获取数据的行列数  返回元组
print(data.shape)
# 获取数据信息
print(data.info())
# 获取数据分布
print(data.describe())

print('------------保存为excel-------------')
# index=False 不保存索引值 na_rep 空值用0填充  无穷大值用1填充 如2/0
data.to_excel('result.xlsx', sheet_name='xxx', index=False, na_rep=0, inf_rep=1)
