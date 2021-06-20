class Animal:
    def eat(self):
        print("动物都得吃")


class Dog(Animal):
    def eat(self):
        print("Dog 吃肉")


class Cat(Animal):
    def eat(self):
        print("cat eat mouse")


class Person(Animal):
    def eat(self):
        print("human eat rice")


def fun(obj):
    obj.eat()


fun(Dog())
fun(Cat())
fun(Person())
