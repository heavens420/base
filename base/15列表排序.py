lst = [3, 45, 23, 654, 23, 43, 12]

# 排序 升序  sort() 在原列表上排序不产生新对象
lst.sort()

# 降序
lst.sort(reverse=True)

print(lst)

# sorted() 产生新对象排序
print(lst, id(lst))
lst2 = sorted(lst)

# 降序
lst2 = sorted(lst2, reverse=True)
print(lst2, id(lst2))
