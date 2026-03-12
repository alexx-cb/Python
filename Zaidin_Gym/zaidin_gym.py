from typing import Callable


class ZaidinGym:
    __lista_usuarios = []
    __lista_actividades = []

    def main(self):
        print("Bienvenido a ZaidinGym")
        ZaidinGym.menu_principal()

        opcion =0

        opciones_principales = {
            1: self._gestionar_usuarios(),
            2: self._gestionar_actividades(),
            3: self._consultas_estadisticas()
        }

        while opcion != 4:
            ZaidinGym.menu_principal()

            try:
                opcion = int(input("Introduce una opcion: ").strip())


            except ValueError:
                print("Introduce una opcion valida")
                continue

            if opcion == 4:
                print("saliendo del programa")
                break

            accion = opciones_principales.get(opcion)
            if accion:
                accion()

            else:
                print("Introduce una opcion del menú")

    def _gestionar_usuarios(self)->None:
        """
        Funcion que inicializa el menu de funciones para la gestion de usuarios
        :return: None
        """
        opciones_usuarios = {
            1: self._alta_persona,
            2: self._baja_persona,
            3: self._gestionar_socios,
            4: self._gestionar_monitores,
            5: self._inactivar_socios
        }

        self._ejecutar_menu(ZaidinGym.menu_gestion_usuarios, opciones_usuarios, 6)


    def _gestionar_socios(self)->None:
        """
        Funcion que inicializa el menu de funciones para la gestion de socios
        :return: None
        """
        opciones_socios = {
            1: self._mostrar_lista_actividades,
            2: self._añadir_actividad,
            3: self._eliminar_actividad,
            4: self._valorar_actividad,
            5: self._convertir_premium
        }

        self._ejecutar_menu(ZaidinGym.menu_gestion_socios, opciones_socios, 6)


    @staticmethod
    def _ejecutar_menu(menu_func: Callable[[], None],opciones: dict,opcion_salida: int) -> None:
        """
        Funcion que valida la entrada de datos en los menús para evitar la duplicidad y ejecuta la accion correspondiente
        :param menu_func:Callable [] con menu que contiene las opciones validas, devuelve None
        :param opciones: Dict con las funciones para cada opcion
        :param opcion_salida: int con el valor para salir de la funcion
        :return: None
        """
        opcion =0
        while opcion != opcion_salida:
            menu_func()

            try:
                opcion = int(input("Introduce una opcion: ").strip())

            except ValueError:
                print("Introduce una opcion valida")
                continue

            if opcion == opcion_salida:
                break

            accion = opciones.get(opcion)
            if accion:
                accion()
            else:
                print("Introduce una opcion valida")

    @staticmethod
    def menu_principal():
        print("\n1. Gestionar usuarios (socios y monitores)")
        print("2. Gestionar actividades")
        print("3. Consultas y estadisticas")
        print("4. Salir")


    @staticmethod
    def menu_gestion_usuarios():
        print("\n1. Alta personas, (socios o monitores)")
        print("2. Baja personas")
        print("3. Gestionar socios")
        print("4. Gestionar monitores")
        print("5. Inactivar socios automaticamente")
        print("6. Volver")


    @staticmethod
    def menu_gestion_socios():
        print("\n1. Mostrar lista de actividades")
        print("2. Añadir actividad")
        print("3. Eliminar actividad")
        print("4. Valorar actividad")
        print("5. Convertir en premium")
        print("6. Volver")

    @staticmethod
    def menu_gestion_actividades():
        print("\n1. Listar personas existentes")
        print("2. Listar las n mejores actividades")
        print("3. Listar las n mejores actividades por categoria")
        print("4. Listar las n mejores actividades por cantidad de kcal")
        print("5. Listar los n mejores monitores")
        print("6. Volver")

if __name__ == "__main__":
    gym = ZaidinGym()
    gym.main()