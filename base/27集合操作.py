s = set([1, 2, 3, 4, 5, 6])

# 集合是无序的 添加后也无序
# 集合添加元素  一次添加一个
s.add(99)

# add one at least once
s.update([22, 33, 44])
print(s)

# 集合删除 不存在报错
s.remove(99)
print(s)

# 存在删除 不存在不报错
s.discard(888)
print(s)

# 删除任意元素
s.pop()
print(s)

# 清空集合
s.clear()
print(s)
