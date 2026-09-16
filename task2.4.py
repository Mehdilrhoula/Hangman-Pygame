import turtle

radius=0

for i in range(20):
    turtle.circle(radius, 180)
    radius = radius + 20

turtle.exitonclick()