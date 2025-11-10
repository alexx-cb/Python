# Escribe un programa que muestre por pantalla una lista de 10 números enteros generados al azar
# entre 0 y 100. A continuación, el programa debe pedir un número al usuario. Se debe comprobar que el
# número introducido por teclado se encuentra dentro de la lista, en caso contrario se mostrará un
# mensaje por pantalla y se volverá a pedir un número; así hasta que el usuario introduzca uno
# correctamente. A continuación, el programa rotará la lista hacia la derecha las veces que haga falta
# hasta que el número introducido quede situado en la posición 0 de la lista. Por último, se mostrará la
# lista rotada por pantalla.
import random
from collections import deque

numeros = []

for i in range(0,10):
    numeros.append(random.randint(0,100))

print(numeros)


objetivo = int(input("introduce un numero que este en la lista: "))

while objetivo not in numeros:
    print("numero invalido")
    objetivo = int(input("introduce un numero que este en la lista: "))


indice = numeros.index(objetivo)

deque_numeros = deque(numeros)

deque_numeros.rotate(-indice)
numeros = deque_numeros

print(list(numeros))

