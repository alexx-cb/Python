# Realizar un programa que defina un vector llamado “vector_numeros” de 10 enteros, a continuación
# lo inicialice con valores aleatorios (del 1 al 10) y posteriormente muestre en pantalla cada elemento del
# vector junto con su cuadrado y su cubo.

import random

vector_numeros= []

for i in range(1,11):
    aleatorio = random.randint(0,100)
    vector_numeros.append(aleatorio)


for i in range(0, len(vector_numeros)):
    print("numero: ",vector_numeros[i], "cuadrado: ",vector_numeros[i]**2, "cubo: ",vector_numeros[i]**3)

