score = dict(name='zhagnsan', age=20)

# 方式1：
print(score['name'])

# 找不到报错
# print(score['dd'])

# 方式2：
print(score.get('name'))

# 找不到返回None
print(score.get('hh'))

# 找不到设置默认值
print(score.get('hh', '默认值'))
