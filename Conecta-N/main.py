import random

CASILLA_VACIA =0
FICHA_CIRCULO = 1
FICHA_EQUIS=2

FICHAS_LINEA = 4

NOMBRE1=""
NOMBRE2=""
MODO=""
DIFICULTAD=0


def main():
    """
    Funcion principal del programa que permite el juego de JcJ y JcM

    :return: void
    """
    modo_juego()
    tablero = crear_tablero()

    jugadores = {
        FICHA_EQUIS: NOMBRE1,
        FICHA_CIRCULO: NOMBRE2,
    }

    turno = FICHA_EQUIS
    mostrar_tablero(tablero)

    while True:

        jugador_nombre = jugadores[turno]


        print("Turno de ", jugador_nombre)

        if MODO in ["MÁQUINA", "MAQUINA"] and turno == FICHA_CIRCULO:
            colocar_aleatorio(tablero, turno)
        else:

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


        ganador = comprobar_linea(tablero, columna-1, FICHAS_LINEA)

        if ganador:
            print(f"PARTIDA FINALIZADA\n"
                  f"HA GANADO: {jugador_nombre}\n")

            break
        elif not hay_casillas_libres(tablero):
            print(f"PARTIDA FINALIZADA\n"
                  f"HAY UN EMPATE")

            break

        turno = FICHA_CIRCULO if turno == FICHA_EQUIS else FICHA_EQUIS


def colocar_aleatorio(tablero, ficha):
    columna_aleatoria = random.randint(0, len(tablero[0]))
    colocar_ficha(tablero, columna_aleatoria, ficha)

def hay_casillas_libres(tablero):
    """
    Funcion que devuelve si hay casillas libres restantes en el tablero

    :param tablero: Tablero actual de la partida
    :return: True si todavia hay casillas libres, False si no
    """

    for fila in tablero:
        for casilla in fila:
            if casilla == CASILLA_VACIA:
                return True

    return False


def contar_fichas_en_direccion(tablero, fila, columna, ficha, df, dc):
    """
    Funcion que devuelve las fichas que hay en linea teniendo en cuenta la ultima ficha colocada

    :param tablero: tablero actual de la partida
    :param fila: fila de la ultima ficha
    :param columna: columna de la ultima ficha
    :param ficha: X o O
    :param df: direccion en filas desde la fila inicial
    :param dc: direccion en columnas desde la columna inicial
    :return: numero de fichas que hay en linea
    """
    filas = len(tablero)
    columnas = len(tablero[0])

    count = 0
    f_actual, c_actual = fila + df, columna + dc

    while (0 <= f_actual < filas and 0 <= c_actual < columnas and
           tablero[f_actual][c_actual] == ficha):
        count += 1
        f_actual += df
        c_actual += dc

    return count


def calcular_max_linea(tablero, fila, columna, ficha):
    """
    Funcion que devulve el maximo numero de fichas que puede haber en linea teniendo en cuenta la ultima ficha colocada

    :param tablero: Tablero actual de la partida
    :param fila: fila de la ultima ficha colocada
    :param columna: columna de la ultima ficha colocada
    :param ficha: X o O
    :return: numero máximo de fichas que puede haber en linea
    """
    direcciones = [
        (0, 1),  # Horizontal derecha
        (1, 0),  # Vertical hacia abajo
        (1, 1),  # Diagonal derecha
        (1, -1)  # Diagonal izquierda
    ]

    max_linea = 0
    for df, dc in direcciones:
        total = 1  # La ficha actual
        total += contar_fichas_en_direccion(tablero, fila, columna, ficha, df, dc)
        total += contar_fichas_en_direccion(tablero, fila, columna, ficha, -df, -dc)

        if total > max_linea:
            max_linea = total

    return max_linea


def comprobar_linea(tablero, columna, numero_fichas_linea):
    """
    Funcion que comprueba si existe una linea ganadora despues de colocar una ficha

    :param tablero: Tablero actual de la partida
    :param columna: columna en la que se ha colocado la ficha
    :param numero_fichas_linea: Constante con el numero de fichas en linea necesarias para ganar la partida
    :return: True si las fichas en linea son mayor o iguales a la constante o False por el contrario
    """
    filas = len(tablero)

    fila = None
    for f in range(filas - 1, -1, -1):
        if tablero[f][columna] != CASILLA_VACIA:
            fila = f
            break

    if fila is None:
        return False

    jugador = tablero[fila][columna]

    max_linea = calcular_max_linea(tablero, fila, columna, jugador)

    return max_linea >= numero_fichas_linea


def fichas_en_linea(tablero, ficha, columna):
    """
    Funcion que devuelve las fichas que hay en linea actualmente

    :param tablero: Tablero actual de la partida
    :param ficha: X o O
    :param columna: columna en la que se ha colocado la ficha
    :return: 0 o numero de fichas que puede haber en linea
    """
    filas = len(tablero)

    if tablero[0][columna] != CASILLA_VACIA:
        return 0

    fila_colocacion = None
    for f in range(filas - 1, -1, -1):
        if tablero[f][columna] == CASILLA_VACIA:
            fila_colocacion = f
            break

    if fila_colocacion is None:
        return 0

    return calcular_max_linea(tablero, fila_colocacion, columna, ficha)

def colocar_ficha(tablero, columna, ficha):
    """
    Funcion que coloca una ficha en el tablero

    :param tablero: Tablero actual de la partida
    :param columna: columna en la que se va a colocar la ficha
    :param ficha: X o O
    :return: True si se ha podido colocar la ficha en el tablero, False por el contrario
    """
    if tablero[0][columna] != CASILLA_VACIA:
        print("La columna está llena, elige otra columna")
        return False

    for fila in range(len(tablero) -1, -1,-1):
        if tablero[fila][columna] == CASILLA_VACIA:
            tablero[fila][columna] = ficha
            return True
    return False


def mostrar_tablero_columna(tablero, columna_ultima_ficha):
    """
    Funcion que muestra el tablero con la ultima columna en la que se ha colocado una ficha resaltada

    :param tablero: Tablero actual de la partida
    :param columna_ultima_ficha: columna en la que se ha colocado la ficha
    :return: void
    """
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
        if i == columna_ultima_ficha-1:
            numeros.append(f"\033[1;33m{i + 1:^3}\033[0m")
        else:
            numeros.append(f"{i + 1:^3}")
    print(f" {' '.join(numeros)}")


    partes_superior = []
    for i in range(columnas):
        if i == columna_ultima_ficha-1:
            partes_superior.append("\033[1;33m───\033[0m")
        else:
            partes_superior.append("───")
    linea_superior = "┌" + "┬".join(partes_superior) + "┐"
    print(linea_superior)


    for i, fila in enumerate(tablero):
        contenido_partes = []
        for j, c in enumerate(fila):
            if j == columna_ultima_ficha-1:
                contenido_partes.append(f"\033[1;33m {simbolos[c]} \033[0m")
            else:
                contenido_partes.append(f" {simbolos[c]} ")
        contenido = "│".join(contenido_partes)
        print(f"│{contenido}│")

        if i < filas - 1:
            partes_separadora = []
            for j in range(columnas):
                if j == columna_ultima_ficha-1:
                    partes_separadora.append("\033[1;33m───\033[0m")
                else:
                    partes_separadora.append("───")
            linea_separadora = "├" + "┼".join(partes_separadora) + "┤"
            print(linea_separadora)

    partes_inferior = []
    for i in range(columnas):
        if i == columna_ultima_ficha-1:
            partes_inferior.append("\033[1;33m───\033[0m")
        else:
            partes_inferior.append("───")
    linea_inferior = "└" + "┴".join(partes_inferior) + "┘"
    print(linea_inferior)
    print()


def mostrar_tablero(tablero):
    """
    Funcion que muesta el tablero

    :param tablero: Tablero actual de la partida
    :return: void
    """
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
    """
    Funcion que crea el tablero en el que se va a jugar

    :return: tablero
    """
    print("Introduce el tamaño del tablero, como mínimo el tablero tendrá unas dimensiones de 6 filas por 7 columnas")

    global FICHAS_LINEA

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

    while True:
        try:
            FICHAS_LINEA = int(input(f"Introduce cuantas fichas en linea quieres que sean necesarias para ganar\n"
                                     f"el mínimo siempre será 4 y como máximo sera la longitud de las columnas: "))


            if FICHAS_LINEA<4:
                FICHAS_LINEA = 4
            elif FICHAS_LINEA>columnas:
                FICHAS_LINEA = columnas

            break

        except:
            print("Ingrese un numero valido")

    tablero = [[CASILLA_VACIA for _ in range(columnas)] for _ in range(filas)]
    return tablero


def modo_juego():
    """
    Funcion que permite elegir el modo de juego, JcJ o JcM y guarda los nombres en constantes

    :return: void
    """
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
        NOMBRE2 = "Máquina"


if __name__ == "__main__":
    main()