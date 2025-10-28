# Pide una cadena y dos caracteres por teclado (valida que sea un carácter), sustituye la aparición del
# primer carácter en la cadena por el segundo carácter

cadena = input("Ingrese cadena: ")

caracter = input("Ingrese el carcter que quiere cambiar: ")

while len(caracter) != 1:
    print("Solo puedes introducir 1 caracter")
    caracter = input("Ingrese el carcter que quiere cambiar: ")


sustituto = input("Ingrese el caracter de cambio: ")

while len(sustituto) != 1:
    print("Solo puedes introducir 1 caracter")
    sustituto = input("Ingrese el caracter de cambio: ")

cadena = cadena.replace(caracter, sustituto)

print(cadena)