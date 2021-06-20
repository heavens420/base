# 元组为不可变集合 即不可增删改

# 元组创建方式1：
tu = ('ni', 'hao', 'a')
print(tu)

# 方式1.5：
tu = 'shi', 'jie', 'hh'
print(tu)

# 元组创建方式2：
tu = tuple(('wo', 'hen', 'hao'))
print(tu, type(tu))

# 如果元组中只有一个元素 逗号不能省略 否则默认为str类型
tu = 'book'
print(tu, type(tu))

tu = 'bool',
tu = ('book',)
print(tu, type(tu))

# 创建空列表
lst = list()
lst = []

# create empty dict
dic = {}
dic = dict()

# create empty tuple
tu = ()
tu = tuple()
