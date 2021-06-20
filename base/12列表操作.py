lst = [1, 2, 3, 4]

# 向列表添加一个元素
lst.append(6)
print(lst)

# 向列表添加一个列表中的所有元素
lst2 = [7, 9, 10]
lst.extend(lst2)

# 向列表中添加一个列表的部分元素
lst.extend(lst2[1:2])

# 向列表中添加一个空列表的元素(不会报错)
lst.extend(lst2[5:])
print(lst)

# 在列表的任意地方添加元素
lst.insert(1, 888)

# 列表中不存在要插入的索引 则索引为正数插到最后  为负数 插到最前
lst.insert(-22, 99)
lst.insert(88, 77)
print(lst)

# 切片 部分替换
lst3 = [12, 34, 56, 78]
lst[1:-2] = lst3

# 切片  将lst从 索引1（包含）开始 用lst2的元素替换
# lst[1:] = lst2

print(lst)
