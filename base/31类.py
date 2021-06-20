class Student:
    native_pace = '定义在类里面的变量称为类属性'

    # 定义构造器
    def __init__(self, name, age):
        self.age = age
        self.name = name

    def eat(self):
        print('类内部定义成为方法')

    @staticmethod
    def eat_again():
        print('定义静态方法')

    @classmethod
    def class_method(cls):
        print('定义类方法')


def eat_again_two():
    print('定义在类外面的方法称为函数')


# 类的使用
# 创建类的实例对象
stu = Student('张三', 20)
# 调用类的方法
stu.eat()
# 通过实例对象调用类属性
print(stu.native_pace)
# 通过实例调用静态方法
stu.eat_again()
# 通过类实例对象调用类方法
stu.class_method()
# 直接通过类名调用类的方法 需要传入类的实例对象
Student.eat(stu)

# 调用类的静态方法
Student.eat_again()

# 调用类方法
Student.class_method()

# 调用类属性
print(Student.native_pace)

# 属性绑定
# 将函数绑定到stu实例
stu.eat_again_two = eat_again_two
# 绑定变量
addr = 'beijing'
stu.addr = addr
# 调用绑定的函数
stu.eat_again_two()
# 调用绑定到stu的变量
print(stu.addr)
