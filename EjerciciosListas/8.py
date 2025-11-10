# Escribe un programa que genere 20 números enteros aleatorios entre 0 y 100 y que los almacene en
# una lista. El programa debe ser capaz de pasar todos los números pares a las primeras posiciones de la
# lista (del 0 en adelante) y todos los números impares a las celdas restantes. Utiliza listas auxiliares si es
# necesario.
import random

numeros = []

for i in range(0,20):
    numeros.append(random.randint(1,100))

pares =[]
impares = []
for i in range(0,len(numeros)):
    if numeros[i]%2 == 0:
        pares.append(numeros[i])
    else:
        impares.append(numeros[i])

numeros = []
for i in range(0,len(pares)):
    numeros.append(pares[i])

for i in range(0,len(impares)):
    numeros.append(impares[i])

print(numeros)