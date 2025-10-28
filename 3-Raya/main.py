VACIO =0
JUGADOR_X = 1
JUGADOR_O = 2


def jugar_tres_en_raya():
    tablero = [[VACIO for _ in range(3)] for _ in range(3)]
    nombre1 = str(input("Ingrese el nombre del jugador 1: ") or "Jugador 1")
    nombre2 = str(input("Ingrese el jugador del jugador 2: ") or "Jugador 2")


    jugadores = {
        JUGADOR_O : nombre2,
        JUGADOR_X : nombre1
    }

    turno = JUGADOR_X

    while True:

        jugador_nombre = jugadores[turno]

        mostrar_tablero(tablero)
        print("Turno del jugador: ", jugador_nombre)

        # FALTA TRY CATCH
        col = int(input("Ingrese la columna (1-3): "))-1
        fila = int(input("Ingrese la linea (1-3): "))-1

        if not colocar_ficha(tablero, fila, col, turno):
            continue

        ganador =hay_ganador(tablero)
        if ganador:
            mostrar_tablero(tablero)
            print("GANA ", jugadores[ganador], "!!")
            break

        turno = JUGADOR_X if turno == JUGADOR_O else JUGADOR_O


def mostrar_tablero(tablero):
    simbolos = {VACIO: " ", JUGADOR_X: "X", JUGADOR_O: "O"}
    for i, fila in enumerate(tablero):
        print(" | ".join(simbolos[c] for c in fila))
        if i < len(tablero) - 1:
            print("-" * 9)


def colocar_ficha(tablero, fila, col, turno):

    if tablero[fila][col] != VACIO:
        print("Esa casilla esta ya cogida, vuelve a intentarlo")
        return
    tablero[fila][col] = turno


def hay_ganador(tablero):
    """
    Revisa si hay un ganador en el tablero.
    Devuelve:
      - JUGADOR_O si gana O,
      - JUGADOR_X si gana X,
      - None si no hay ganador todavía.
    """
    n = len(tablero)

    for fila in tablero:
        if fila.count(fila[0]) == n and fila[0] != VACIO:
            return fila[0]

    for c in range(n):
        columna = [tablero[r][c] for r in range(n)]
        if columna.count(columna[0]) == n and columna[0] != VACIO:
            return columna[0]

    diag1 = [tablero[i][i] for i in range(n)]
    if diag1.count(diag1[0]) == n and diag1[0] != VACIO:
        return diag1[0]

    diag2 = [tablero[i][n - 1 - i] for i in range(n)]
    if diag2.count(diag2[0]) == n and diag2[0] != VACIO:
        return diag2[0]

    return None

jugar_tres_en_raya()