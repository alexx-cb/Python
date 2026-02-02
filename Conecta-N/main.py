import random
import os


class Constantes:
    """Clase para almacenar las constantes del juego"""
    CASILLA_VACIA = 0
    FICHA_CIRCULO = 1
    FICHA_EQUIS = 2
    FICHAS_LINEA_DEFAULT = 4
    MIN_FILAS = 6
    MIN_COLUMNAS = 7
    MIN_FICHAS_LINEA = 4


class Tablero:
    """Clase que representa el tablero de juego"""

    def __init__(self, filas, columnas, fichas_linea):
        self.filas = filas
        self.columnas = columnas
        self.fichas_linea = fichas_linea
        self.grid = [[Constantes.CASILLA_VACIA for _ in range(columnas)] for _ in range(filas)]

    def colocar_ficha(self, columna, ficha):
        """Coloca una ficha en la columna especificada"""
        if self.grid[0][columna] != Constantes.CASILLA_VACIA:
            print("La columna está llena, elige otra columna")
            return False

        for fila in range(self.filas - 1, -1, -1):
            if self.grid[fila][columna] == Constantes.CASILLA_VACIA:
                self.grid[fila][columna] = ficha
                return True
        return False

    def hay_casillas_libres(self):
        """Verifica si quedan casillas libres en el tablero"""
        for fila in self.grid:
            for casilla in fila:
                if casilla == Constantes.CASILLA_VACIA:
                    return True
        return False

    def comprobar_linea(self, columna):
        """Comprueba si hay una línea ganadora después de colocar ficha"""
        fila = None
        for f in range(self.filas):
            if self.grid[f][columna] != Constantes.CASILLA_VACIA:
                fila = f
                break

        if fila is None:
            return False

        jugador = self.grid[fila][columna]
        max_linea = self._calcular_max_linea(fila, columna, jugador)

        return max_linea >= self.fichas_linea

    def fichas_en_linea(self, ficha, columna):
        """Calcula cuántas fichas en línea se obtendrían al colocar en columna"""
        if self.grid[0][columna] != Constantes.CASILLA_VACIA:
            return 0

        fila_colocacion = None
        for f in range(self.filas - 1, -1, -1):
            if self.grid[f][columna] == Constantes.CASILLA_VACIA:
                fila_colocacion = f
                break

        if fila_colocacion is None:
            return 0

        self.grid[fila_colocacion][columna] = ficha
        max_linea = self._calcular_max_linea(fila_colocacion, columna, ficha)
        self.grid[fila_colocacion][columna] = Constantes.CASILLA_VACIA

        return max_linea

    def _calcular_max_linea(self, fila, columna, ficha):
        """Calcula el máximo de fichas en línea desde una posición"""
        direcciones = [
            (0, 1),  # Horizontal derecha
            (1, 0),  # Vertical hacia abajo
            (1, 1),  # Diagonal derecha
            (1, -1)  # Diagonal izquierda
        ]

        max_linea = 0
        for df, dc in direcciones:
            total = 1
            total += self._contar_fichas_en_direccion(fila, columna, ficha, df, dc)
            total += self._contar_fichas_en_direccion(fila, columna, ficha, -df, -dc)

            if total > max_linea:
                max_linea = total

        return max_linea

    def _contar_fichas_en_direccion(self, fila, columna, ficha, df, dc):
        """Cuenta fichas consecutivas en una dirección"""
        count = 0
        f_actual, c_actual = fila + df, columna + dc

        while (0 <= f_actual < self.filas and
               0 <= c_actual < self.columnas and
               self.grid[f_actual][c_actual] == ficha):
            count += 1
            f_actual += df
            c_actual += dc

        return count

    def mostrar(self, columna_resaltada=None):
        """Muestra el tablero, opcionalmente resaltando una columna"""
        simbolos = {
            Constantes.CASILLA_VACIA: " ",
            Constantes.FICHA_CIRCULO: "O",
            Constantes.FICHA_EQUIS: "X",
        }

        print()

        # Números de columnas
        numeros = []
        for i in range(self.columnas):
            if columna_resaltada is not None and i == columna_resaltada - 1:
                numeros.append(f"\033[1;33m{i + 1:^3}\033[0m")
            else:
                numeros.append(f"{i + 1:^3}")
        print(f" {' '.join(numeros)}")

        # Línea superior
        partes_superior = []
        for i in range(self.columnas):
            if columna_resaltada is not None and i == columna_resaltada - 1:
                partes_superior.append("\033[1;33m───\033[0m")
            else:
                partes_superior.append("───")
        linea_superior = "┌" + "┬".join(partes_superior) + "┐"
        print(linea_superior)

        # Filas
        for i, fila in enumerate(self.grid):
            contenido_partes = []
            for j, c in enumerate(fila):
                if columna_resaltada is not None and j == columna_resaltada - 1:
                    contenido_partes.append(f"\033[1;33m {simbolos[c]} \033[0m")
                else:
                    contenido_partes.append(f" {simbolos[c]} ")
            contenido = "│".join(contenido_partes)
            print(f"│{contenido}│")

            if i < self.filas - 1:
                partes_separadora = []
                for j in range(self.columnas):
                    if columna_resaltada is not None and j == columna_resaltada - 1:
                        partes_separadora.append("\033[1;33m───\033[0m")
                    else:
                        partes_separadora.append("───")
                linea_separadora = "├" + "┼".join(partes_separadora) + "┤"
                print(linea_separadora)

        # Línea inferior
        partes_inferior = []
        for i in range(self.columnas):
            if columna_resaltada is not None and i == columna_resaltada - 1:
                partes_inferior.append("\033[1;33m───\033[0m")
            else:
                partes_inferior.append("───")
        linea_inferior = "└" + "┴".join(partes_inferior) + "┘"
        print(linea_inferior)
        print()


class Jugador:
    """Clase base para representar un jugador"""

    def __init__(self, nombre, ficha):
        self.nombre = nombre
        self.ficha = ficha

    def obtener_movimiento(self, tablero):
        """Método que debe ser implementado por las subclases"""
        raise NotImplementedError


class JugadorHumano(Jugador):
    """Jugador humano que ingresa movimientos por teclado"""

    def obtener_movimiento(self, tablero):
        """Solicita al jugador que ingrese una columna"""
        while True:
            try:
                columna = int(input("Ingrese la columna en la que quiere colocar la ficha: "))

                while columna < 1 or columna > tablero.columnas:
                    print(f"La columna no existe, debe estar entre 1 y {tablero.columnas}")
                    columna = int(input("Ingrese la columna en la que quiere colocar la ficha: "))

                return columna - 1
            except:
                print("Ingrese un numero de columna válido")


class JugadorMaquina(Jugador):
    """Jugador controlado por IA"""

    def __init__(self, nombre, ficha, dificultad):
        super().__init__(nombre, ficha)
        self.dificultad = dificultad

    def obtener_movimiento(self, tablero):
        """Obtiene el movimiento de la máquina según su dificultad"""
        if self.dificultad == 1:
            return self._movimiento_facil(tablero)
        elif self.dificultad == 2:
            return self._movimiento_dificil(tablero)

    @staticmethod
    def _movimiento_facil(tablero):
        """Modo fácil: movimiento aleatorio"""
        columnas_disponibles = [col for col in range(tablero.columnas)
                                if tablero.grid[0][col] == Constantes.CASILLA_VACIA]
        if columnas_disponibles:
            return random.choice(columnas_disponibles)
        return None

    def _movimiento_dificil(self, tablero):
        """Modo difícil: estrategia inteligente"""
        ficha_oponente = (Constantes.FICHA_EQUIS if self.ficha == Constantes.FICHA_CIRCULO
                          else Constantes.FICHA_CIRCULO)

        # 1. ¿Puedo ganar?
        columna = self._buscar_columna_ganar_bloquear(tablero, self.ficha)
        if columna is not None:
            return columna

        # 2. ¿Bloquear al jugador?
        columna = self._buscar_columna_ganar_bloquear(tablero, ficha_oponente)
        if columna is not None:
            return columna

        # 3. Columna con más fichas en línea
        columna = self._buscar_mejor_columna(tablero)
        if columna is not None:
            return columna

        # 4. Aleatorio
        return self._movimiento_facil(tablero)

    @staticmethod
    def _buscar_columna_ganar_bloquear(tablero, ficha):
        """Busca una columna para ganar o bloquear"""
        for col in range(tablero.columnas):
            if tablero.fichas_en_linea(ficha, col) >= tablero.fichas_linea:
                return col
        return None

    def _buscar_mejor_columna(self, tablero):
        """Busca la columna con más fichas en línea posibles"""
        mejores_columnas = []
        max_fichas = 0

        for col in range(tablero.columnas):
            fichas = tablero.fichas_en_linea(self.ficha, col)

            if fichas > max_fichas:
                max_fichas = fichas
                mejores_columnas = [col]
            elif fichas == max_fichas and fichas > 0:
                mejores_columnas.append(col)

        if mejores_columnas:
            return random.choice(mejores_columnas)
        return None


class Juego:
    """Clase principal que controla el flujo del juego"""

    ARCHIVO_PARTIDA = "partida_conecta4.txt"

    def __init__(self):
        self.tablero = None
        self.jugadores = []
        self.turno_actual = 0
        self.modo = None

    def configurar(self):
        """Configura el juego: modo, jugadores y tablero"""
        # Verificar si existe una partida guardada
        if self.existe_partida_guardada():
            respuesta = input("Se ha encontrado una partida guardada. ¿Desea continuar? (s/n): ").lower()
            if respuesta == 's':
                self.cargar_partida()
                return
            else:
                # Eliminar partida guardada si se inicia una nueva
                if os.path.exists(self.ARCHIVO_PARTIDA):
                    os.remove(self.ARCHIVO_PARTIDA)

        # Nueva partida
        self.modo = self._seleccionar_modo()
        self._crear_jugadores(self.modo)
        self.tablero = self._crear_tablero()

    def existe_partida_guardada(self):
        """Comprueba si existe un archivo de partida guardada"""
        return os.path.exists(self.ARCHIVO_PARTIDA)

    def cargar_partida(self):
        """Carga una partida desde el archivo guardado"""
        try:
            with open(self.ARCHIVO_PARTIDA, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()


                config_tablero = lineas[0].strip().split(',')
                filas = int(config_tablero[0])
                columnas = int(config_tablero[1])
                fichas_linea = int(config_tablero[2])


                self.tablero = Tablero(filas, columnas, fichas_linea)


                self.modo = lineas[1].strip()


                datos_j1 = lineas[2].strip().split(',')
                nombre_j1 = datos_j1[0]
                ficha_j1 = int(datos_j1[1])

                datos_j2 = lineas[3].strip().split(',')
                nombre_j2 = datos_j2[0]
                ficha_j2 = int(datos_j2[1])
                tipo_j2 = datos_j2[2]  # "HUMANO" o "MAQUINA"

                jugador1 = JugadorHumano(nombre_j1, ficha_j1)
                self.jugadores.append(jugador1)

                if tipo_j2 == "HUMANO":
                    jugador2 = JugadorHumano(nombre_j2, ficha_j2)
                else:
                    dificultad = int(datos_j2[3])
                    jugador2 = JugadorMaquina(nombre_j2, ficha_j2, dificultad)
                self.jugadores.append(jugador2)

                self.turno_actual = int(lineas[4].strip())

                for i in range(filas):
                    fila_datos = lineas[5 + i].strip().split(',')
                    for j in range(columnas):
                        self.tablero.grid[i][j] = int(fila_datos[j])

                print(f"\n¡Partida cargada correctamente!")
                print(f"Continúa el turno de {self.jugadores[self.turno_actual].nombre}\n")

        except Exception as e:
            print(f"Error al cargar la partida: {e}")
            print("Iniciando una nueva partida...")
            self.modo = self._seleccionar_modo()
            self._crear_jugadores(self.modo)
            self.tablero = self._crear_tablero()

    def guardar_partida(self):
        """Guarda el estado actual de la partida en un archivo"""
        try:
            with open(self.ARCHIVO_PARTIDA, 'w', encoding='utf-8') as archivo:
                archivo.write(f"{self.tablero.filas},{self.tablero.columnas},{self.tablero.fichas_linea}\n")

                archivo.write(f"{self.modo}\n")

                j1 = self.jugadores[0]
                archivo.write(f"{j1.nombre},{j1.ficha}\n")

                j2 = self.jugadores[1]
                if isinstance(j2, JugadorMaquina):
                    archivo.write(f"{j2.nombre},{j2.ficha},MAQUINA,{j2.dificultad}\n")
                else:
                    archivo.write(f"{j2.nombre},{j2.ficha},HUMANO\n")


                archivo.write(f"{self.turno_actual}\n")


                for fila in self.tablero.grid:
                    archivo.write(','.join(str(celda) for celda in fila) + '\n')

                archivo.flush()
                os.fsync(archivo.fileno())

            print("Partida guardada correctamente.")

        except Exception as e:
            print(f"Error al guardar la partida: {e}")

    def eliminar_partida_guardada(self):
        """Elimina el archivo de partida guardada"""
        try:
            if os.path.exists(self.ARCHIVO_PARTIDA):
                os.remove(self.ARCHIVO_PARTIDA)
                print("Archivo de partida eliminado.")
        except Exception as e:
            print(f"Error al eliminar la partida: {e}")

    @staticmethod
    def _seleccionar_modo():
        """Permite al usuario seleccionar el modo de juego"""
        print("Elige un modo de juego (Jugador vs Jugador o Jugador vs Máquina): ")

        while True:
            try:
                modo = input("Escribe 'Jugador' o 'Máquina': ").upper()
                if modo in ['JUGADOR', 'MAQUINA', 'MÁQUINA']:
                    return modo
                print("Introduce un modo válido")
            except:
                print("Ingrese un modo válido")

    def _crear_jugadores(self, modo):
        """Crea los jugadores según el modo seleccionado"""
        nombre1 = input("Ingrese el nombre del jugador 1: ")
        jugador1 = JugadorHumano(nombre1, Constantes.FICHA_EQUIS)
        self.jugadores.append(jugador1)

        if modo == 'JUGADOR':
            nombre2 = input("Ingrese el nombre del jugador 2: ")
            jugador2 = JugadorHumano(nombre2, Constantes.FICHA_CIRCULO)
            self.jugadores.append(jugador2)
        else:
            while True:
                try:
                    dificultad = int(input("Ingrese la dificultad de la maquina '1' o '2', (1-Facil / 2-Dificil): "))
                    if 1 <= dificultad <= 2:
                        jugador2 = JugadorMaquina("Máquina", Constantes.FICHA_CIRCULO, dificultad)
                        self.jugadores.append(jugador2)
                        break
                    print("La dificultad debe ser 1 o 2")
                except ValueError:
                    print("Ingrese un valor válido para la dificultad '1' o '2'")

    @staticmethod
    def _crear_tablero():
        """Crea el tablero con las dimensiones especificadas"""
        print(
            "Introduce el tamaño del tablero, como mínimo el tablero tendrá unas dimensiones de 6 filas por 7 columnas")

        while True:
            try:
                filas = int(input("Ingrese las filas del tablero: "))
                columnas = int(input("Ingrese las columnas del tablero: "))

                if filas < Constantes.MIN_FILAS:
                    filas = Constantes.MIN_FILAS
                if columnas < Constantes.MIN_COLUMNAS:
                    columnas = Constantes.MIN_COLUMNAS

                break
            except:
                print("Ingrese un numero valido")

        while True:
            try:
                fichas_linea = int(input(f"Introduce cuantas fichas en linea quieres que sean necesarias para ganar\n"
                                         f"el mínimo siempre será 4 y como máximo sera la longitud de las columnas: "))

                if fichas_linea < Constantes.MIN_FICHAS_LINEA:
                    fichas_linea = Constantes.MIN_FICHAS_LINEA
                elif fichas_linea > columnas:
                    fichas_linea = columnas

                break
            except:
                print("Ingrese un numero valido")

        return Tablero(filas, columnas, fichas_linea)

    def jugar(self):
        """Ejecuta el bucle principal del juego"""
        self.tablero.mostrar()

        while True:
            jugador_actual = self.jugadores[self.turno_actual]
            print(f"Turno de {jugador_actual.nombre}")

            # Obtener movimiento
            columna_indice = jugador_actual.obtener_movimiento(self.tablero)

            if columna_indice is None:
                continue

            # Colocar ficha
            if not self.tablero.colocar_ficha(columna_indice, jugador_actual.ficha):
                continue

            # Mostrar información del movimiento de la máquina
            if isinstance(jugador_actual, JugadorMaquina):
                print(f"La máquina coloca en la columna {columna_indice + 1}")

            # Mostrar tablero
            self.tablero.mostrar(columna_indice + 1)

            # Comprobar ganador
            if self.tablero.comprobar_linea(columna_indice):
                print(f"PARTIDA FINALIZADA\n"
                      f"HA GANADO: {jugador_actual.nombre}\n")
                self.eliminar_partida_guardada()
                break

            # Comprobar empate
            if not self.tablero.hay_casillas_libres():
                print(f"PARTIDA FINALIZADA\n"
                      f"HAY UN EMPATE")
                self.eliminar_partida_guardada()
                break

            # Cambiar turno
            self.turno_actual = 1 - self.turno_actual

            self.guardar_partida()

    def iniciar(self):
        """Método principal para iniciar el juego"""
        self.configurar()
        self.jugar()


def main():
    """Función principal del programa"""
    juego = Juego()
    juego.iniciar()


if __name__ == "__main__":
    main()