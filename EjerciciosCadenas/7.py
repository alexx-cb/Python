# Realizar un programa que lea una cadena por teclado y convierta las mayúsculas a minúsculas y
# viceversa.

print("Programa que invierte mayusculas y minusculas")
cadena = input("Ingrese una cadena: ")

for letra in cadena:
    if letra.islower():
        cambiada = letra.upper()
        cadena = cadena.replace(letra, cambiada)
    else:
        cambiada = letra.lower()
        cadena = cadena.replace(letra,cambiada)


print(cadena)