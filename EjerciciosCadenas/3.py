# Realizar un programa que comprueba si una cadena leída por teclado comienza por una subcadena introducida por teclado.

cadena = input("Introduce una cadena: ")
subcadena = input("Introduce la subcadena: ")

if cadena[:len(subcadena)] == subcadena:
    print("La cadena comienza por la subcadena")
else:
    print("La cadena NO comienza por la subcadena")