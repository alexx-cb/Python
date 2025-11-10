CASILLA_VACIA =0
FICHA_CIRUCLO = 1
FICHA_EQUIS=2

def crear_tablero():
    print("Introduce el tamaño del tablero, como mínimo el tablero tendrá unas dimensiones de 6 filas por 7 columnas")

    while True:
        try:
            filas = int(input("Ingrese las filas del tablero: "))
            columnas = int(input("Ingrese las columnas del tablero: "))


            break
        except:
            print("Ingrese un numero valido")



crear_tablero()