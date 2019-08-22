#Program to make a circle out of consecutive squares
import turtle

def draw_square(some_turtle):
    for i in range(1,5):
        some_turtle.forward(100)
        some_turtle.right(90)

def draw_art():
     window=turtle.Screen()
     window.bgcolor("red")
    # Let brad be ' some_turtle'
     brad=turtle.Turtle()
     brad.shape("turtle")
     brad.color("yellow")
     brad.speed(5)
     for i in range(1,37):
         draw_square(brad)
         brad.right(10)

     window.exitonclick()

draw_art()
