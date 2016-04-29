import turtle
pen = turtle.Turtle()
x = 0
y = 0
pos = (x,y)
x = 10
y = 5
for i in range(50):

    pen.undo()
    pen.ht()
    pen.speed(0)
    pen.color("blue")

    pen.up()
    pen.setpos(pos)
    pen.down()
    pen.dot(50)

    pos = (pos[0] + x, pos[0] + y)


turtle.mainloop()
#=========================================================================
import turtle
import random as r

def popWalls(turtle, wallNum, wallSize):

    for i in range(wallNum):
        pos = (r.randint(-1000, 1000), r.randint(-1000, 1000))
        turtle.up()
        turtle.setpos(pos)

        turtle.down()

        turtle.fill(1)
        turtle.fd(wallSize/2)
        turtle.rt(90)
        turtle.fd(wallSize)
        turtle.rt(90)
        turtle.fd(wallSize/2)
        turtle.rt(90)
        turtle.fd(wallSize)
        turtle.fill(0)

#test script-----------------------
obs = turtle.Turtle()
obs.speed(100)
obs.hideturtle()
obs.color("blue")

popWalls(obs, 10, 250)

turtle.mainloop()
#-----------------------------------