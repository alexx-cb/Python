contador = 0
suma_impares = 0
contador_impares = 0
mayor_par = None

while True:
    numero = int(input("Introduce un número (negativo para terminar): "))
    if numero < 0:
        break

    contador += 1

    if numero % 2 == 0:
        if mayor_par is None or numero > mayor_par:
            mayor_par = numero
    else:
        suma_impares += numero
        contador_impares += 1

print(f"\nSe han introducido {contador} números en total.")

if contador_impares > 0:
    media_impares = suma_impares / contador_impares
    print(f"La media de los números impares es: {media_impares:.2f}")
else:
    print("No se han introducido números impares.")

if mayor_par is not None:
    print(f"El mayor de los números pares es: {mayor_par}")
else:
    print("No se han introducido números pares.")