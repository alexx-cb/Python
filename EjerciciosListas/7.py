# Escribe un programa que genere 100 números aleatorios del 0 al 20 y que los muestre por pantalla
# separados por espacios. El programa pedirá entonces por teclado dos valores y a continuación cambiará
# todas las ocurrencias del primer valor por el segundo en la lista generada anteriormente. Los números
# que se han cambiado deben aparecer entrecomillados
import random

numeros = []

for i in range(0,100):
    numeros.append(random.randint(0,20))


lista_bonita= " ".join([str(i) for i in numeros])


print(lista_bonita)


antiguo = int(input("Que número quieres cambiar?: "))
nuevo = int(input("Porque numero quieres que cambie: "))

for i in range(0,len(numeros)):
    if numeros[i] == antiguo:
        numeros[i]= nuevo

lista_bonita= " ".join([str(i) for i in numeros])

print(lista_bonita)