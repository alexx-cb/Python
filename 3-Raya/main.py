import os

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
    ARCHIVO_PARTIDA = "partida_guardada.txt"

    def __init__(self):
        self.tablero = Tablero()
        self.jugador1 = None
        self.jugador2 = None
        self.turno = None

        if self.existe_partida_guardada():
            respuesta = input("Se ha encontrado una partida guardada. ¿Desea continuar? (s/n): ").lower()
            if respuesta == 's':
                self.cargar_partida()
            else:
                self.nueva_partida()

                if os.path.exists(self.ARCHIVO_PARTIDA):
                    os.remove(self.ARCHIVO_PARTIDA)
        else:
            self.nueva_partida()

    def existe_partida_guardada(self):
        return os.path.exists(self.ARCHIVO_PARTIDA)

    def nueva_partida(self):
        self.jugador1 = Jugador(input("Ingrese el nombre del jugador 1: ") or "Jugador 1", self.JUGADOR_O)
        self.jugador2 = Jugador(input("Ingrese el nombre del jugador 2: ") or "Jugador 2", self.JUGADOR_X)
        self.turno = self.jugador1

    def cargar_partida(self):
        try:
            with open(self.ARCHIVO_PARTIDA, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()

                nombre_jugador1 = lineas[0].strip()
                nombre_jugador2 = lineas[1].strip()

                self.jugador1 = Jugador(nombre_jugador1, self.JUGADOR_O)
                self.jugador2 = Jugador(nombre_jugador2, self.JUGADOR_X)

                turno_simbolo = int(lineas[2].strip())
                self.turno = self.jugador1 if turno_simbolo == self.JUGADOR_O else self.jugador2


                for i in range(3):
                    fila_datos = lineas[3 + i].strip()
                    for j in range(3):
                        self.tablero.celdas[i][j] = int(fila_datos[j])

                print(f"\n¡Partida cargada correctamente!")
                print(f"Continúa el turno de {self.turno.nombre}\n")

        except Exception as e:
            print(f"Error al cargar la partida: {e}")
            print("Iniciando una nueva partida...")
            self.nueva_partida()

    def guardar_partida(self):
        try:
            with open(self.ARCHIVO_PARTIDA, 'w', encoding='utf-8') as archivo:
                archivo.write(f"{self.jugador1.nombre}\n")
                archivo.write(f"{self.jugador2.nombre}\n")

                archivo.write(f"{self.turno.simbolo}\n")


                for fila in self.tablero.celdas:
                    archivo.write(''.join(str(celda) for celda in fila) + '\n')

                archivo.flush()
                os.fsync(archivo.fileno())

            print("Partida guardada correctamente.")

        except Exception as e:
            print(f"Error al guardar la partida: {e}")

    def eliminar_partida_guardada(self):
        try:
            if os.path.exists(self.ARCHIVO_PARTIDA):
                os.remove(self.ARCHIVO_PARTIDA)
                print("Archivo de partida eliminado.")
        except Exception as e:
            print(f"Error al eliminar la partida: {e}")

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
                self.eliminar_partida_guardada()
                break

            if self.tablero.hay_empate():
                self.tablero.mostrar_tablero()
                print("EMPATE!")
                self.eliminar_partida_guardada()
                break

            self.cambiar_turno()

            self.guardar_partida()

if __name__ == "__main__":
    J = Juego()
    J.jugar()