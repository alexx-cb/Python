positivos = 0
negativos = 0

for i in range(1, 11):
    numero = float(input(f"Introduce el número {i}: "))
    if numero > 0:
        positivos += 1
    elif numero < 0:
        negativos += 1

print(f"\nCantidad de números positivos: {positivos}")
print(f"Cantidad de números negativos: {negativos}")