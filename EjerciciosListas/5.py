# Diseñar el algoritmo correspondiente a un programa, que:
# • Crea una tabla bidimensional de longitud 5x5 y nombre ‘matriz’.
# • Carga la tabla con valores numéricos enteros.
# • Suma todos los elementos de cada fila y todos los elementos de cada columna visualizando
# los resultados en pantalla.
import random

matriz = [[random.randint(1,100) for _ in range(5)] for _ in range(5)]



for linea in matriz:
    suma = sum(linea)
    print(linea,"= " ,suma)

for i in range(5):
    suma =0
    for linea in matriz:

        digito = linea[i]
        suma += digito
    print(suma, end=" ")
