# 11 Validacion de archivo con permisos
try:
    with open("archivo_protegido.txt", "wt") as archivo:
        archivo.write("Intentando escribir en el archivo")

    print("Archivo escrito correctamente.")

except PermissionError:
    print("Error: no tienes permisos para escribir en este archivo.")

except FileNotFoundError:
    print("Error: el archivo o la ruta no existen.")

# Cifrado / Descifrado basico de archivos
def cifrar_archivo(origen, destino, clave):
    with open(origen, "rt") as archivo:
        texto = archivo.read()

    texto_cifrado = ""
    for caracter in texto:
        texto_cifrado += chr(ord(caracter) + clave)

    with open(destino, "wt") as archivo:
        archivo.write(texto_cifrado)

    print("Archivo cifrado correctamente.")


def descifrar_archivo(origen, destino, clave):
    with open(origen, "rt") as archivo:
        texto_cifrado = archivo.read()

    texto_descifrado = ""
    for caracter in texto_cifrado:
        texto_descifrado += chr(ord(caracter) - clave)

    with open(destino, "wt") as archivo:
        archivo.write(texto_descifrado)

    print("Archivo descifrado correctamente.")


clave = int(input("Ingrese la clave numérica: "))

cifrar_archivo("mensaje.txt", "mensaje_cifrado.txt", clave)
descifrar_archivo("mensaje_cifrado.txt", "mensaje_descifrado.txt", clave)