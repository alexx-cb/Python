# Realiza un programa que pinte la letra U por pantalla hecha con asteriscos. El programa pedirá la
# altura. Fíjate que el programa inserta un espacio y pinta dos asteriscos menos en la base para simular la
# curvatura de las esquinas inferiores.

altura = int(input("Introduce la altura de la U: "))

for i in range(altura - 1):
    print(" * " + " " * (altura) + " * ")

print("  " + " *" * (altura - 2) + " ")