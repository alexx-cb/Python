import json
import os

from tarjeta_credito import TarjetaCredito
from movimiento import Movimiento
from database.database import DataBase, TarjetaDB, MovimientosDB

class AplicacionTarjetaCredito:

    PATH = "tarjetas.json"
    def __init__(self)->None:
        """
        Constructor de la clase AplicacionTarjetaCredito \n

        Inicializa una list para agregar las TarjetaCredito y la base de datos
        """
        self.lista_tarjetas = []
        self.db = DataBase()
        self.tarjeta_db = TarjetaDB(self.db)
        self.movimientos_db = MovimientosDB(self.db)

    def main(self)->None:
        """
        Funcion principal del programa \n

        Ejecuta las funciones según lo ordene el usuario
        :return: None
        """
        opcion =0

        # Cargar tarjetas desde la base de datos
        self.cargar_tarjetas_db()

        # Código comentado para persistencia JSON
        # self.cargar_tarjetas(self.PATH)

        opciones = {
            1: lambda: self.agregar_tarjeta(),
            2: lambda: self.eliminar_tarjeta_nif(),
            3: lambda: self.gestionar_tarjeta(input("Introduce el nif de la tarjeta: ")),
            4: lambda: print(self.gasto_total_tarjetas())
        }

        while opcion != 5:
            AplicacionTarjetaCredito.mostrar_menu()
            try:
                opcion = int(input("Introduce una opcion: ").strip())

            except ValueError:
                print("Introduce una opcion valida")
                continue

            if opcion == 5:
                # Código comentado para persistencia JSON
                # self.guardar_json(self.PATH)
                print("Saliendo del programa. Los datos están guardados en la base de datos.")
                break

            accion = opciones.get(opcion)
            if accion:
                accion()
            else:
                print("Opcion no valida, introduce una opcion valida")

        self.db.close()

    def cargar_tarjetas_db(self):
        """
        Carga todas las tarjetas desde la base de datos
        """
        try:
            tarjetas_rows = self.tarjeta_db.select_all()
            self.lista_tarjetas = []

            for row in tarjetas_rows:
                numero_tarjeta = row[0]
                movimientos_rows = self.movimientos_db.select_by_tarjeta(numero_tarjeta)
                movimientos = []

                for mov_row in movimientos_rows:
                    movimientos.append(Movimiento(
                        cantidad=mov_row[2],
                        concepto=mov_row[3],
                        fecha=mov_row[4]
                    ))


                tarjeta = TarjetaCredito.from_db_row(row, movimientos)
                self.lista_tarjetas.append(tarjeta)

            print(f"Se han cargado {len(self.lista_tarjetas)} tarjetas desde la base de datos")
        except Exception as e:
            print(f"Error al cargar tarjetas de la base de datos: {e}")
            self.lista_tarjetas = []

    # Funciones comentadas para persistencia JSON
    """
    def cargar_tarjetas(self, path):
        if not os.path.exists(path):
            self.lista_tarjetas = []
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    self.lista_tarjetas = []
                    return

                data = json.loads(contenido)

            self.lista_tarjetas = [TarjetaCredito.from_dict(t) for t in data]

        except json.JSONDecodeError as e:
            print(f"Error al cargar el archivo de tarjetas: {e}")
            self.lista_tarjetas = []

    def guardar_json(self, path):
        try:
            data = [t.to_dict() for t in self.lista_tarjetas]

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"Error al guardar las tarjetas: {e}")
    """

    def agregar_tarjeta(self)->None:
        """
        Funcion que agrega a la list de tarjetas la nueva tarjeta de credito si se ha creado correctamente
        :return: None
        """
        try:
            tarjeta = self.crear_tarjeta()
            if tarjeta:
                self.lista_tarjetas.append(tarjeta)

                if self.tarjeta_db.insert(tarjeta):
                    print("Tarjeta creada correctamente y guardada en la base de datos")
                else:
                    print("Tarjeta creada pero hubo un error al guardarla en la base de datos")
                    self.lista_tarjetas.pop()
        except ValueError as e:
            print(f"Error al crear la tarjeta: {e}")

    def buscar_tarjeta(self, nif: str) -> int | None:
        """
        Funcion que recibe por parámetro un nif de la tarjeta a buscar y devuelve la posicion en la que se encuentra
        en la list de tarjetas o None si no encuentra la tarjeta
        :param nif: str con el nif asociado a la tarjeta
        :return: int | None
        """
        for index, tarjeta in enumerate(self.lista_tarjetas):
            if tarjeta.nif == nif:
                return index

        return None

    def eliminar_tarjeta(self,index:int) -> bool:
        """
        Funcion que recibe por parametro una posición en el list de tarjetas y la elimina \n
        devuelve True si se ha eliminado
        :param index: int con la posición en el list de tarjetas
        :return: bool
        """
        try:
            tarjeta = self.lista_tarjetas[index]
            if self.tarjeta_db.delete(tarjeta.card_number):
                self.lista_tarjetas.pop(index)
                return True
            else:
                print("Error al eliminar de la base de datos")
                return False
        except IndexError:
            return False

    def eliminar_tarjeta_nif(self) -> bool:
        """
        Funcion que ejecuta las funciones de buscar y eliminar en el flujo del programa
        :return: bool
        """
        nif = input("Introduce el nif de la tarjeta a eliminar")

        index = self.buscar_tarjeta(nif)

        if index is None:
            print("No se ha encontrado la tarjeta asociada a ese nif")
            return False

        self.eliminar_tarjeta(index)
        print(f"Se ha eliminado la tarjeta asociada a {nif}")
        return True

    def gasto_total_tarjetas(self)-> float:
        """
        Funcion que recorre el list de tarjetas y devuelve la sumatoria de todos los pagos realizados por todas las
        tarjetas
        :return: float
        """
        suma =0
        for tarjeta in self.lista_tarjetas:
            individual = self.gasto_total(tarjeta)

            suma += individual

        print("El gasto total de las tarjetas es: ")
        return suma

    def gestionar_tarjeta(self, nif: str) -> TarjetaCredito | None | str:
        """
        Funcion que recibe por parametro un nif para poder gestionar en específico una tarjeta dentro del flujo del
        programa. \n

        LLama a otras funciones dependiendo de lo que decida el usuario
        :param nif: str con el nif asociado a una tarjeta de credito
        :return: TarjetaCredito | str | None
        """
        index = self.buscar_tarjeta(nif)
        if index is None:
            print("No se ha encontrado la tarjeta asociada a ese NIF")
            return

        tarjeta = self.lista_tarjetas[index]

        opciones = {
            1: lambda: print("Numero de la tarjeta: "+str(tarjeta.card_number)),
            2: lambda: print("Titular: " +str(tarjeta.holder)),
            3: lambda: print("Fecha de caducidad: " + str(tarjeta.expiration_month) + "/" + str(tarjeta.expiration_year)),
            4: lambda: self._modificar_pin(tarjeta),
            5: lambda: self._realizar_pago(tarjeta),
            6: lambda: self._consultar_movimientos(tarjeta),
            7: lambda: print(self.gasto_total(tarjeta))
        }

        opcion =0
        while opcion != 8:
            self.mostrar_menu_gestion_tarjeta()

            try:
                opcion = int(input("Seleccione una opción: "))
            except ValueError:
                print("Opcion no valida, introduce un numero del 1 - 8")
                continue

            if opcion == 8:
                break

            accion = opciones.get(opcion)
            if accion:
                accion()
            else:
                print("Opcion no valida, introduce un numero del 1 - 8")

    @staticmethod
    def gasto_total(tarjeta: TarjetaCredito)->float:
        """
        Static Method que devuelve el gasto total de la tarjeta
        :param tarjeta: TarjetaCredito
        :return: float
        """
        return TarjetaCredito.gastado(tarjeta)

    def _modificar_pin(self, tarjeta: TarjetaCredito) -> bool:
        """
        Modifica el pin de la tarjeta devuelve True si se ha modificado con éxito
        :param tarjeta: TarjetaCredito
        :return: bool
        """
        while True:
            new = input("Introduce el pin nuevo (mínimo 4 dígitos): ")
            if new.isdigit() and len(new) >= 4:
                try:
                    nuevo_pin = int(new)
                    if self.tarjeta_db.update_pin(tarjeta.card_number, nuevo_pin):
                        tarjeta.pin = nuevo_pin
                        print("Pin modificado correctamente")
                        return True
                    else:
                        print("Error al actualizar el PIN en la base de datos")
                        return False
                except ValueError as e:
                    print(f"Error: {e}")
                    return False
            else:
                print("El PIN debe tener al menos 4 dígitos numéricos")

    def _realizar_pago(self, tarjeta: TarjetaCredito) -> bool:
        """
        Static Method que permite realizar un pago con una tarjeta siempre y cuando no supere el límite de pago de la tarjeta
        :param tarjeta: TarjetaCredito
        :return: bool
        """
        if tarjeta.numero_movimientos() == 0:
            total_gastado = 0
        else:
            total_gastado = tarjeta.gastado()

        limite_restante = tarjeta.limit - total_gastado
        print(f"El límite restante de la tarjeta es: {limite_restante}€")

        while True:
            try:
                pago = float(input("Introduce la cantidad del pago: "))
                if pago <= 0:
                    print("Introduce un número mayor que 0")
                    continue
                if pago > limite_restante:
                    print(f"No se puede realizar el pago. El límite restante es {limite_restante}€")
                    continue
                break
            except ValueError:
                print("Introduce un número válido para el pago")

        while True:
            concepto = input("Introduce el concepto (5 - 50 caracteres): ").strip()
            if 5 <= len(concepto) <= 50:
                break
            print("El concepto debe tener entre 5 y 50 caracteres")

        try:
            tarjeta.pagar(pago, concepto)
            movimiento = tarjeta.movements[-1]
            if self.movimientos_db.insert(movimiento, tarjeta.card_number):
                print(f"Pago realizado con éxito: {pago}€ - {concepto}")
                return True
            else:
                print("Pago registrado en memoria pero error al guardar en la base de datos")
                return False
        except ValueError as e:
            print(f"No se pudo realizar el pago: {e}")
            return False

    @staticmethod
    def _consultar_movimientos(tarjeta :TarjetaCredito)->None:
        """
        Static Method que muestra los n últimos movimientos de la tarjeta
        :param tarjeta: TarjetaCredito
        :return: None
        """
        numero = tarjeta.numero_movimientos()

        if numero == 0:
            print("La tarjeta de credito no tiene movimientos")
            return

        print(f"la lista de movimientos tiene una longitud de: {numero}")
        print("Cuantos movimientos quiere comprobar?, se mostraran primero los últimos movimientos realizados")

        while True:
            try:
                n = int(input("Introduce un numero de movimientos: "))
                if 0 <= n <= numero:
                    break
            except ValueError:
                pass
            print(f"Introduce un numero válido entre 0 y {numero}")


        lista = tarjeta.movimientos(n)
        print("\nMovimientos de la tarjeta:")

        for item in lista:
            print(item)

    def existe_tarjeta_nif(self, nif: str) -> bool:
        """
        Funcion que comprueba si el nif ya existe en la tarjeta
        :param nif: str con el nif de la futura tarjeta
        :return: bool
        """
        # Verificar tanto en memoria como en la base de datos
        if any(tarjeta.nif == nif for tarjeta in self.lista_tarjetas):
            return True
        return self.tarjeta_db.exists_nif(nif)

    def crear_tarjeta(self) -> TarjetaCredito | None:
        """
        Funcion que muestra el flujo para crear una tarjeta de credito \n

        Devuelve un objeto nuevo con todos los parámetros introducidos
        :return: TarjetaCredito | None
        """
        print("\nIntroduce los siguientes datos para crear tarjeta")

        holder = input("Titular (15 - 80 caracteres): ")
        nif = input("NIF, CIF o NIE: ")

        if self.existe_tarjeta_nif(nif):
            print("Ya existe una tarjeta asociada a ese NIF")
            return None

        pin = int(input("PIN (4 dígitos minimo): "))
        limit = int(input("Limite de pago (500 - 5000): "))
        card_num = int(input("Numero de la tarjeta de crédito (16 digitos): "))

        return TarjetaCredito(holder, nif, pin, limit, card_num)

    @staticmethod
    def mostrar_menu()->None:
        """
        Static Method que muestra por consola el menú principal del programa
        :return: None
        """
        print("\n--- MENÚ TARJETAS DE CRÉDITO ---")
        print("1. Crear tarjeta de crédito.")
        print("2. Eliminar tarjeta de crédito.")
        print("3. Gestionar tarjeta de crédito.")
        print("4. Consultar gastos totales.")
        print("5. Salir del programa")

    @staticmethod
    def mostrar_menu_gestion_tarjeta()->None:
        """
        Static Method que muestra por consola el menú de gestion de una tarjeta en específico
        :return: None
        """
        print("\n--- GESTIÓN DE TARJETA DE CRÉDITO ---")
        print("1. Mostrar el número de tarjeta completo.")
        print("2. Mostrar el nombre del titular de la tarjeta.")
        print("3. Mostrar la fecha de caducidad.")
        print("4. Modificar el PIN.")
        print("5. Realizar un pago.")
        print("6. Consultar movimientos.")
        print("7. Consultar gasto total.")
        print("8. Volver al menú principal.")


if __name__ == "__main__":
    AplicacionTarjetaCredito().main()
