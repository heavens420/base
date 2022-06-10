import pandas as pd

data = pd.DataFrame(['a', 'b', 'c'])
print(data)
print('-----------------------------------------------------')
# 每一个列表都是一行
data = pd.DataFrame([['q', 'w', 'e'], ['a', 's', 'd']])
print(data)
print('----------------------------------------------------')
# 指定列名和索引编号
data3 = pd.DataFrame([['q', 'w', 'e'], ['a', 's', 'd']], columns=['c1', 'c2', 'c3'], index=['a', 'b'])
print(data3)
print('------------------------------------------------------')
# 每一个字典都是一列
# data2 = pd.DataFrame({'no1': ['q', 'w', 'e'], 'no2': ['a', 's', 'd']})
data2 = pd.DataFrame({'no1': ['q', 'w', 'e'], 'no2': ['a', 's', 'd']}, index=[3, 6, 9])
print(data2)
print(f'--->>>{list(data2)}')
print('------------------------------------------------------------')
print(data2.columns)
print(data2.values)
print(data2.index)
