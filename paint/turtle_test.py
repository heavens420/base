# coding=utf-8
import turtle
import clock


def five_star():
    turtle.pensize(5)
    turtle.pencolor("blue")
    turtle.fillcolor("green")

    turtle.begin_fill()
    for _ in range(5):
        turtle.forward(200)
        turtle.right(144)
    turtle.end_fill()
    clock.sleep(2)

    turtle.penup()
    turtle.goto(-150, -120)
    turtle.color("violet")
    turtle.write("Done", font=('Arial', 40, 'normal'))

    turtle.mainloop()


def xiang_ri_kui():
    # 同时设置pencolor=color1, fillcolor=color2
    turtle.color("red", "yellow")
    turtle.begin_fill()
    for _ in range(50):
        turtle.forward(200)
        turtle.left(170)
    turtle.end_fill()

    turtle.mainloop()


xiang_ri_kui()
