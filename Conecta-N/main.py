CASILLA_VACIA =0
FICHA_CIRUCLO = 1
FICHA_EQUIS=2

NOMBRE1=""
NOMBRE2=""
MODO=""


def main():
    modo_juego()
    tablero = crear_tablero()
    mostrar_tablero(tablero)


def mostrar_tablero(tablero):
    simbolos = {
        CASILLA_VACIA: " ",
        FICHA_CIRUCLO: "O",
        FICHA_EQUIS: "X",
    }

    filas = len(tablero)
    columnas = len(tablero[0])

    print()

    numeros = " ".join(f"{i + 1:^3}" for i in range(columnas))
    print(f" {numeros}")

    linea_superior = "┌" + "┬".join(["───"] * columnas) + "┐"
    print(linea_superior)

    for i, fila in enumerate(tablero):
        contenido = "│".join(f" {simbolos[c]} " for c in fila)
        print(f"│{contenido}│")

        if i < filas - 1:
            linea_separadora = "├" + "┼".join(["───"] * columnas) + "┤"
            print(linea_separadora)

    linea_inferior = "└" + "┴".join(["───"] * columnas) + "┘"
    print(linea_inferior)
    print()

def crear_tablero():
    print("Introduce el tamaño del tablero, como mínimo el tablero tendrá unas dimensiones de 6 filas por 7 columnas")

    while True:
        try:
            filas = int(input("Ingrese las filas del tablero: "))
            columnas = int(input("Ingrese las columnas del tablero: "))

            if filas<6:
                filas = 6
            if columnas<7:
                columnas = 7

            break
        except:
            print("Ingrese un numero valido")

    tablero = [[CASILLA_VACIA for _ in range(columnas)] for _ in range(filas)]
    return tablero


def modo_juego():
    print("Elige un modo de juego (Jugador vs Jugador o Jugador vs Máquina): ")

    global MODO
    global NOMBRE1


    try:
        MODO = input("Escribe 'Jugador' o 'Máquina': ")
    except:
        print("Ingrese un modo válido")


    MODO = MODO.upper()

    while MODO not in ['JUGADOR', 'MAQUINA', 'MÁQUINA']:
        print("Introduce un modo valido")
        MODO = input("Escribe 'Jugador' o 'Máquina': ")


    if MODO == 'JUGADOR':
        global NOMBRE2

        NOMBRE1 = input("Ingrese el nombre del jugador 1: ")
        NOMBRE2 = input("Ingrese el nombre del jugador 2: ")

    elif MODO in ['MAQUINA', 'MÁQUINA']:
        NOMBRE1 = input("Ingrese el nombre del jugador: ")


if __name__ == "__main__":
    main()