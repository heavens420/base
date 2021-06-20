class Human:
    def what(self):
        print("I am Human")


class Person:
    def say(self):
        print("Person")


class Student(Person):
    def say(self):
        print("Student子类重写Person")


class Teacher(Human, Person):
    def what(self):
        print("重写Human")

    def say(self):
        print("重写Person")


teacher = Teacher()
teacher.say()
teacher.what()
