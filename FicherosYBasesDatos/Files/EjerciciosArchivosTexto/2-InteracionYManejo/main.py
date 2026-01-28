from pathlib import Path

# 4 Guardar Entradas del Usuario (con \n)
with open("perfiles.txt", "at") as file:
    while True:
        nombre = input("Ingrese su nombre: ")
        edad = input("Ingrese su edad: ")
        ciudad = input("Ingrese su ciudad: ")

        file.write(f"nombre: {nombre}\n")
        file.write(f"edad: {edad}\n")
        file.write(f"ciudad: {ciudad}\n")
        file.write("\n")

        opcion = input("¿Desea ingresar otro perfil? (s/n): ").lower()
        if opcion != "s":
            break

# 5 Contador de Caracteres (WordCounter Básico)
def contador(nombre_archivo):
    with open(nombre_archivo, "rt") as archivo1:
        info = archivo1.read()

    info = info.replace("\n", "")
    return len(info)


print("Palabras en el archivo 'perfiles.txt'", contador("perfiles.txt"))

# 6 Listado y Busqueda de archivos
directorio = Path(".")

print("Archivos en el directorio actual:")
for archivo in directorio.glob("*"):
    print(archivo.name)

# Buscar un archivo
nombre = input("\nIngrese el nombre del archivo a buscar: ")

archivo_buscar = Path(nombre)

if archivo_buscar.exists():
    print(f"El archivo '{nombre}' fue encontrado.")
else:
    print(f"El archivo '{nombre}' NO existe.")


# 7 Especificando codificacion
try:
    with open("latin.txt", "rt", encoding="utf-8") as archivo:
        contenido = archivo.read()
        print("Contenido del archivo:\n")
        print(contenido)

except UnicodeDecodeError:
    print("Error: el archivo no pudo ser leído con la codificación UTF-8.")