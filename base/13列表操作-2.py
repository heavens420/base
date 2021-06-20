lst = [1, 2, 3, 4, 5, 6, 7]

# 移除某个元素,不存在则 报错
lst.remove(2)

# 移除某个索引对于的元素
lst.pop(0)

# 不给参数 默认移除最后一个
lst.pop()

# 切片方式删除 可参考上个demo
lst[1:3] = []

# 清空元素
lst.clear()

# 删除元素 删除之后使用改列表引用报错 未定义
del lst

print(lst)
