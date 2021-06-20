# 集合自动去重,元素位置无序

# 方式1：
s1 = {'a', 'b', 'c'}
print(s1, type(s1))

# 方式2：
s2 = set(range(6))
print(s2)

# 方式3： 将列表元素转集合
s3 = set(['e', 'r', 't', 't'])
print(s3)

# 方式4：将元组转化为集合
s4 = set(('qw', 'er', 'er', 'wqwee'))
print(s4)

# 空集合
s5 = set()
print(s5, type(s5))

# 空字典
s6 = {}
print(s6, type(s6))
