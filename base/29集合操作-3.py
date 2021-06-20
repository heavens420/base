s1 = {1, 2, 3, 4}
s2 = {2, 3, 4, 5}

# 交集
print(s1.intersection(s2))
print(s1 & s2)

# 并集
print(s1.union(s2))
print(s1 | s2)

# 差集
print(s1.difference(s2))
print(s2.difference(s1))

# 对称差集 即交集的补集 也即差集的并集
print(s1.symmetric_difference(s2))
