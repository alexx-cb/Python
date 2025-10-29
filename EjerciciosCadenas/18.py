# Realiza un programa que pinte una X hecha de asteriscos. El programa debe pedir la altura. Se debe
# comprobar que la altura sea un número impar mayor o igual a 3, en caso contrario se debe mostrar un
# mensaje de error.

altura = int(input("Introduce la altura de la X (impar, mínimo 3): "))

while altura < 3 or altura % 2 == 0:
    print("La altura debe ser un numero impar")
    altura = int(input("Introduce la altura de la X: "))


for i in range(altura):
    for j in range(altura):
        if i == j or j == (altura - i - 1):
            print("*", end="")
        else:
            print(" ", end="")
    print()