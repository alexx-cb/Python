class Tablero:
    VACIO =0

    def __init__(self, dimension =3):
        self.dimension = dimension
        self.celdas = [[self.VACIO for _ in range(dimension)] for _ in range(dimension)]

    def mostrar_tablero(self):
        simbolos = {0: " ", 1: "X", 2: "O"}
        for i, fila in enumerate(self.celdas):
            print(" | ".join(simbolos[c] for c in fila))
            if i < self.dimension - 1:
                print("-" * 9)

    def colocar_ficha(self, fila, columna, simbolo):
        if self.celdas[fila][columna] != self.VACIO:
            print("Esta casilla ya esta ocupada")
            return False

        self.celdas[fila][columna] = simbolo
        return True


    def hay_ganador(self):
        n = self.dimension

        for fila in self.celdas:
            if fila.count(fila[0]) == n and fila[0] != self.VACIO:
                return fila[0]

        for c in range(n):
            columna = [self.celdas[r][c] for r in range(n)]
            if columna.count(columna[0]) == n and columna[0] != self.VACIO:
                return columna[0]

        diagonal1 = [self.celdas[i][i] for i in range(n)]
        if diagonal1.count(diagonal1[0]) == n and diagonal1[0] != self.VACIO:
            return diagonal1[0]

        diagonal2 = [self.celdas[i][n-1-i] for i in range(n)]
        if diagonal2.count(diagonal2[0]) == n and diagonal2[0] != self.VACIO:
            return diagonal2[0]

        return None


    def hay_empate(self):
        for fila in self.celdas:
            if self.VACIO in fila:
                return False
        return self.hay_ganador() is None


class Jugador:
    def __init__(self, nombre, simbolo):
        self.nombre = nombre
        self.simbolo = simbolo

class Juego:
    JUGADOR_O = 1
    JUGADOR_X = 2

    def __init__(self):

        self.tablero = Tablero()
        self.jugador1 = Jugador(input("Ingrese el nombre del jugador 1: ") or "Jugador 1", self.JUGADOR_O)
        self.jugador2 = Jugador(input("Ingrese el nombre del jugador 2: ") or "Jugador 2", self.JUGADOR_X)
        self.turno = self.jugador1


    def cambiar_turno(self):
        self.turno = (self.jugador2 if self.turno == self.jugador1 else self.jugador1)


    def jugar(self):
        while True:
            self.tablero.mostrar_tablero()
            print(f"Turno de {self.turno.nombre}")

            while True:
                try:
                    fila = int(input("Fila (1-3): ")) - 1
                    columna = int(input("Columna (1-3): ")) - 1
                    if 0 <= fila <= 2 and 0 <= columna <= 2:
                        break
                    else:
                        print("Los valores deben estar entre 1 y 3")
                except ValueError:
                    print("Debes introducir números")

            if not self.tablero.colocar_ficha(fila, columna, self.turno.simbolo):
                continue

            ganador = self.tablero.hay_ganador()

            if ganador:
                self.tablero.mostrar_tablero()
                nombre = (self.jugador1.nombre if ganador == self.jugador1.simbolo else self.jugador2.nombre)

                print(f"¡GANA {nombre}!")
                break

            if self.tablero.hay_empate():
                self.tablero.mostrar_tablero()
                print("EMPATE!")
                break

            self.cambiar_turno()


if __name__ == "__main__":
    J = Juego()
    J.jugar()