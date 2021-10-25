import pandas as pd

# Series 相当于excel的列
data = pd.Series([10, 23, 45, 65, 65])

print(f'索引 列值\n{data}')

# 对列的值进行操作
data *= 2
print(f'索引 列值\n{data}')

# 列值元素比较
data = data == 20
print(data)

print(f'最大值:{data.max()}')
print(f'最小值:{data.min()}')
print(f'中位数:{data.median()}')
print(f'平均值:{data.mean()}')
print(f'总和:{data.sum()}')
print(f'乘积:{data.prod()}')
print(f'标准差:{data.std()}')
print(f'最大2值:\n{data.nlargest(2)}')
print(f'最小2值:\n{data.nsmallest(2)}')

print('--------------字符串类型Series---------------')
str_data = pd.Series(['你好', '北京', '世界', '很大', 'Hello', 'World'])
# 使用自定义索引
str_data2 = pd.Series(['你好', '北京', '世界', '很大', 'Hello', 'World'], index=[2, 4, 6, 8, 10, 12])
# 字典
str_data3 = pd.Series({1: '你好', 2: '北京', 3: '世界', 4: '很大', 5: 'Hello', 6: 'World'})

print(str_data.str.lower())
print(str_data.str.upper())
print(str_data.str.len())
print(str_data.str.cat(sep=','))
print(str_data.str.contains('Wor'))
print(str_data.str.replace('你好', 'henhao'))

# 获取索引
print(str_data2.index)
# 获取值
print(str_data2.values)

print(f'--------------------dataFrame----------------------')
# 构建dataFrame
data = pd.DataFrame({
    "name": ["zs", "lisi", "wangwu"],
    "salary": [200, 300, 500]
})

print(data)

# 相对于excel表格而言  否则恰好相反
# 取得特定的列
print('------特定的列-------')
series = data['name']
print(series)

print('--------特定的行--------')
row = data.iloc[0]
print(row)
