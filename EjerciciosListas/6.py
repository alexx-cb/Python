# Escribe un programa que lea 15 números por teclado y que los almacene en una lista. Rota los
# elementos de esa lista, es decir, el elemento de la posición 0 debe pasar a la posición 1, el de la 1 a la 2,
# etc. El número que se encuentra en la última posición debe pasar a la posición 0. Finalmente, muestra
# el contenido de la lista.
from collections import deque

lista = []
for i in range(0,15):
    lista.append(int(input(f"Ingrese el numero {i+1}: ")))

print(lista)

deque_lista = deque(lista)
deque_lista.rotate(1)
print(list(deque_lista))
