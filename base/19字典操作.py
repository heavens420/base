score = dict(name='nihao', age=22)
print(score)

# key 的判断 key存在为true 不存在为false
print('age' in score)

# 删除键值对
del score['age']
print(score)

# 添加键值对
score['addr'] = '北京故宫'
print(score)

# 修改键值对
score['addr'] = '河西那百年'
print(score)
