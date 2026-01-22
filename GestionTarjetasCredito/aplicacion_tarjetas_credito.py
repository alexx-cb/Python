from tarjeta_credito import TarjetaCredito

class AplicacionTarjetaCredito:

    def __init__(self):
        self.lista_tarjetas = []

    @staticmethod
    def main()->None:
        AplicacionTarjetaCredito.mostrar_menu()


    def buscar_tarjeta(self, nif: str) -> TarjetaCredito | None:
        for tarjeta in self.lista_tarjetas:
            if tarjeta.nif == nif:
                return tarjeta

        return None

    def eliminar_tarjeta(self, nif: str) -> bool:
        for tarjeta in self.lista_tarjetas:
            if tarjeta.nif == nif:
                self.lista_tarjetas.remove(tarjeta)
                return True
        return False

    def gestionar_tarjeta(self, nif: str) -> TarjetaCredito | None | str:

        tarjeta = self.buscar_tarjeta(nif)
        if not tarjeta:
            print("No se ha encontrado la tarjeta asociada a ese NIF")
            return

        opciones = {
            1: lambda: print("Numero de la tarjeta: "+tarjeta.card_number),
            2: lambda: print("Titular: " +tarjeta.holder),
            3: lambda: print("Fecha de caducidad: " + tarjeta.expiration_month + "/" + tarjeta.expiration_year),
            4: lambda: self._modificar_pin(tarjeta),
            5: lambda: self._realizar_pago(tarjeta),
            6: lambda: self._consultar_movimientos(tarjeta),
            7: lambda: print(tarjeta.gasto_total())
        }

        opcion =0
        while opcion != 8:
            self.mostrar_menu_gestion_tarjeta()

            try:
                opcion = int(input("Seleccione una opción"))
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
    def _consultar_movimientos(tarjeta :TarjetaCredito):
        numero = tarjeta.numero_movimientos()

        if numero == 0:
            print("La tarjeta de credito no tiene movimientos")


        print("la lista de movimientos tiene una longitud de: " + numero)
        print("Cuantos movimientos quiere comprobar?, se mostraran primero los últimos movimientos realizados")

        n =0
        while n < 0 or n > numero:


            try:
                n = int(input("Introduce un numero de movimientos: "))
                break
            except ValueError:
                print(f"Introduce un numero válido entre 0 y {numero}")
                continue


        lista = tarjeta.movimientos(n)
        print("Movimientos de la tarjeta")

        for item in lista:
            print(item)



    @staticmethod
    def crear_tarjeta()->TarjetaCredito:
        print("Introduce los siguientes datos para crear tarjeta")
        holder = input("Titular (15 - 80 caracteres): ")
        nif = input("NIF, CIF o NIE: ")
        pin = input("PIN (4 dígitos minimo): ")
        limit = input("Limite de pago (500 - 5000): ")
        card_num = int(input("Numero de la tarjeta de crédito (16 digitos): "))

        return TarjetaCredito(holder, nif, pin, limit, card_num)



    @staticmethod
    def mostrar_menu()->None:
        print("\n--- MENÚ TARJETAS DE CRÉDITO ---")
        print("1. Crear tarjeta de crédito.")
        print("2. Eliminar tarjeta de crédito.")
        print("3. Gestionar tarjeta de crédito.")
        print("4. Consultar gastos totales.")
        print("5. Salir del programa")

    @staticmethod
    def mostrar_menu_gestion_tarjeta()->None:
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
