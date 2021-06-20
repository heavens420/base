score = dict(name='nihao', age=333)

print(score)

# 获取字典所有的key
keys = score.keys()
print(keys, type(keys))

# 将keys转换为列表
print(list(keys))

# 获取字典中的所有value
values = score.values()
print(values, type(values))

# 将values转换为列表
print(list(values))

# 获取字典中的所有key和value  结果为一个个元组组成
items = score.items()
print(items, type(items))

# 将items转化为 列表
print(list(items))
