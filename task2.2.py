print(on demande d'importer la fonction turtle, d'afficher un écran qu'on va appeler toto lui attribuer un fond noir, ensuite on crée un nouveau curseur qu'on appelle titi
de couleur rouge, et on commence une boucle qui nous permet de faire 3 triangles apres etre allé a droite de 90.
Ensuite on affiche le resultat et on le fige tant qu'on a pas cliqué')

import turtle
toto = turtle.Screen()
toto.bgcolor("black")
titi = turtle.Turtle()
titi.color("red")
for i in range(3):
    titi.right(90)
    titi.circle(42)
toto.exitonclick()