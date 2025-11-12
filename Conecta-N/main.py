CASILLA_VACIA =0
FICHA_CIRCULO = 1
FICHA_EQUIS=2

NOMBRE1=""
NOMBRE2=""
MODO=""


def main():
    modo_juego()
    tablero = crear_tablero()

    jugadores = {
        FICHA_EQUIS: NOMBRE1,
        FICHA_CIRCULO: NOMBRE2,
    }

    turno = FICHA_CIRCULO

    while True:

        jugador_nombre = jugadores[turno]

        mostrar_tablero(tablero)
        print("Turno de ", jugador_nombre)

        while True:
            try:
                columna = int(input("Ingrese la columna en la que quiere colocar la ficha: "))

                while columna < 1 or columna > len(tablero[0]):
                    print(f"La columna no existe, debe estar entre 1 y {len(tablero[0])}")
                    columna = int(input("Ingrese la columna en la que quiere colocar la ficha: "))

                break

            except:
                print("Ingrese un numero de columna válido")


        if not colocar_ficha(tablero, columna-1, turno):
            continue

        mostrar_tablero_columna(tablero, columna)

        turno = FICHA_CIRCULO if turno == FICHA_EQUIS else FICHA_EQUIS




def colocar_ficha(tablero, columna, ficha):
    for fila in range(len(tablero) -1, -1,-1):
        if tablero[fila][columna] == CASILLA_VACIA:
            tablero[fila][columna] = ficha
            return True
    return False


def mostrar_tablero_columna(tablero, columna_ultima_ficha):
    simbolos = {
        CASILLA_VACIA: " ",
        FICHA_CIRCULO: "O",
        FICHA_EQUIS: "X",
    }

    filas = len(tablero)
    columnas = len(tablero[0])

    print()

    numeros = []
    for i in range(columnas):
        if i == columna_ultima_ficha:
            numeros.append(f"\033[1;33m{i + 1:^3}\033[0m")
        else:
            numeros.append(f"{i + 1:^3}")
    print(f" {' '.join(numeros)}")


    partes_superior = []
    for i in range(columnas):
        if i == columna_ultima_ficha:
            partes_superior.append("\033[1;33m───\033[0m")
        else:
            partes_superior.append("───")
    linea_superior = "┌" + "┬".join(partes_superior) + "┐"
    print(linea_superior)


    for i, fila in enumerate(tablero):
        contenido_partes = []
        for j, c in enumerate(fila):
            if j == columna_ultima_ficha:
                contenido_partes.append(f"\033[1;33m {simbolos[c]} \033[0m")
            else:
                contenido_partes.append(f" {simbolos[c]} ")
        contenido = "│".join(contenido_partes)
        print(f"│{contenido}│")

        if i < filas - 1:
            partes_separadora = []
            for j in range(columnas):
                if j == columna_ultima_ficha:
                    partes_separadora.append("\033[1;33m───\033[0m")
                else:
                    partes_separadora.append("───")
            linea_separadora = "├" + "┼".join(partes_separadora) + "┤"
            print(linea_separadora)

    partes_inferior = []
    for i in range(columnas):
        if i == columna_ultima_ficha:
            partes_inferior.append("\033[1;33m───\033[0m")
        else:
            partes_inferior.append("───")
    linea_inferior = "└" + "┴".join(partes_inferior) + "┘"
    print(linea_inferior)
    print()


def mostrar_tablero(tablero):
    simbolos = {
        CASILLA_VACIA: " ",
        FICHA_CIRCULO: "O",
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