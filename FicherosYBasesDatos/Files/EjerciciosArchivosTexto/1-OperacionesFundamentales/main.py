# 1 Escribir y Leer una Línea de Texto
with open("saludo.txt", "wt") as file:
    file.write("Hola me encanta Python")

with open("saludo.txt", "rt") as file:
    print(file.read())

# 2 Añadir un Elemento (Modo Append)
with open("saludo.txt", "at") as file:
    file.write("\nEsta es la segunda linea")

with open("saludo.txt", "rt") as file:
    print(file.read())

# 3 Escritura de Múltiples Líneas
lista = ["Manzanas\n", "Leche\n", "Pan\n"]
with open("lista_compra.txt", "wt") as file:
    file.writelines(lista)

with open("lista_compra.txt", "rt") as file:
    print(file.read())
