import turtle

side = int(input("Combien de côtés voulez-vous ?"))

def draw_polygon(side):
    for i in range(side):
        turtle.forward(150)
        turtle.right(360/side)


draw_polygon(side)
turtle.exitonclick()