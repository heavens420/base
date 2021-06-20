# 查看对象的属性
# print(dir(object))

class A:
    pass


class B:
    pass


class C(A, B):
    def __init__(self, age, name):
        self.age = age
        self.name = name


x = C(21, 'haha')
# 查看实例对象绑定的属性字典
print(x.__dict__)

# 查看类对象的属性方法
print(C.__dict__)

# 查看对象所属类
print(x.__class__)

# 查看当前类的父类
print(C.__bases__)

# 查看类的层次结构
print(C.__mro__)

# 查看子类
print(A.__subclasses__())

