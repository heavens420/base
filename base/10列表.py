# 列表的创建方式 两种
lst = ['we', 'fs', 83]

lst2 = list(['ee', 'vv', 34])

print(lst)
print(lst2)

# 查找索引
print(lst.index('fs'))

# 在指定索引范围查询 左闭右开 索引不存在  报错
# print(lst.index('hhh', 1, 2))

# 根据索引获取元素
print(lst[0])

lst3 = lst2.copy()
lst2.clear()
print(lst3)
