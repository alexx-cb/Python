import csv

# 8 Copiar archivo con manejo de errores
def copiar_archivo(origen, destino):
    try:
        with open(origen, "rt") as archivo_origen:
            contenido = archivo_origen.read()

        with open(destino, "wt") as archivo_destino:
            archivo_destino.write(contenido)

        print("Archivo copiado correctamente.")

    except FileNotFoundError:
        print(f"Error: el archivo '{origen}' no existe.")

copiar_archivo("origen.txt", "destino.txt")

# 9 Simulador de csv
registros = []

with open("datos.csv", "rt", encoding='utf-8') as archivo:
    for linea in archivo:
        linea = linea.strip()  # Quitar espacios y saltos de línea
        if not linea:  # Saltar líneas vacías
            continue

        datos = linea.split(",")

        registro = {
            "producto": datos[0].strip(),
            "cantidad": int(datos[1].strip()),
            "precio": float(datos[2].strip().replace('"', ''))
        }

        registros.append(registro)

print(registros)


# WordCounter
def contar_palabras(nombre_archivo):
    try:
        with open(nombre_archivo, "rt") as archivo:
            texto = archivo.read()

        palabras = texto.split()
        return len(palabras)

    except FileNotFoundError:
        print("El archivo no existe.")
        return 0

total_palabras = contar_palabras("origen.txt")
print("Numero total de palabras", total_palabras)