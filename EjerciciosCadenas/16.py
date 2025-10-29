# Escribe un programa que lea un número n e imprima una pirámide de números con n filas como en
# la siguiente figura

filas = int(input("Ingrese la cantidad de filas: "))

for i in range(1, filas + 1):
    print(" " * (filas - i), end="")

    for j in range(1, i + 1):
        print(j, end="")

    for j in range(i - 1, 0, -1):
        print(j, end="")

    print()