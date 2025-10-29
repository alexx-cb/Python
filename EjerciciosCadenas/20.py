# Realiza un programa que pinte un triángulo hueco tal como se muestra en los ejemplos. El usuario
# debe introducir la altura de la figura

altura = int(input("Introduce la altura del triangulo: "))

while altura <3:
    print("Introduce un triangulo valido")
    altura = int(input("Introduce la altura del triangulo: "))


for i in range(altura, 0, -1):
    if i == altura or i == 1:
        print("*" * i)
    else:
        print("*" + " " * (i-2) + "*")
