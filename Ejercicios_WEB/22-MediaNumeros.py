suma = 0
contador = 0

while True:
    numero = float(input("Introduce un número positivo (negativo para terminar): "))
    if numero < 0:
        break
    suma += numero
    contador += 1

if contador > 0:
    media = suma / contador
    print(f"La media de los números introducidos es: {media:.2f}")
else:
    print("No se ha introducido ningún número positivo.")