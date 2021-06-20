# 元组本身不可变 但其元素如果可变则可变
tu = tuple(('ni', [1, 2, 3], 'ha'))
print(tu, id(tu[1]))

# 修改元组中的可变元素  地址不变
tu[1].append(444)
print(tu, id(tu[1]))

# 修改元组中不可变元素 报错
# tu[0] = 'jjj'
print(tu)
