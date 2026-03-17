from datetime import datetime, date, timedelta
from typing import Callable

from Class.actividad import Actividad
from Class.especialidad import Especialidad
from Class.monitor import Monitor
from Class.socio import Socio
from Class.socio_premium import SocioPremium


class ZaidinGym:
    __lista_usuarios = []
    __lista_actividades = []

    """
    -----------------------------------
                MAIN
    -----------------------------------
    """

    def main(self)->None:
        """
        Funcion principal del programa
        :return: None
        """
        print("Bienvenido a ZaidinGym")

        opcion =0

        opciones_principales = {
            1: self.gestionar_usuarios,
            2: self.gestionar_actividades,
            3: self.consultas_estadisticas
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

    """
    -----------------------------------
            GESTION DE MENUS
    -----------------------------------
    """

    def gestionar_actividades(self) -> None:
        """
        Funcion que inicializa el menu de funciones para la gestion de actividades
        :return: None
        """
        opciones_actividades = {
            1: self.nueva_actividad,
            2: self.eliminar_actividad,
        }

        self._ejecutar_menu(ZaidinGym.menu_actividades,opciones_actividades, 3)

    def gestionar_usuarios(self)->None:
        """
        Funcion que inicializa el menu de funciones para la gestion de usuarios
        :return: None
        """
        opciones_usuarios = {
            1: self.alta_persona,
            2: self.baja_persona,
            3: self.gestionar_socios,
            4: self.gestionar_monitores,
            5: self.inactivar_socios
        }

        self._ejecutar_menu(ZaidinGym.menu_gestion_usuarios, opciones_usuarios, 6)

    def gestionar_socios(self)->None:
        """
        Funcion que inicializa el menu de funciones para la gestion de socios
        :return: None
        """

        dni = input("Introduce el dni del socio: ").strip()
        persona = self._buscar_persona_dni(dni)

        if persona:
            persona.fecha_ultimo_acceso = date.today()

            opciones_socios = {
                1: lambda :self.mostrar_lista_actividades(persona),
                2: lambda :self.nueva_actividad_lista(persona),
                3: lambda :self.eliminar_actividad_lista,
                4: lambda :self.valorar_actividad,
                5: lambda :self.convertir_premium
            }

            self._ejecutar_menu(ZaidinGym.menu_gestion_socios, opciones_socios, 6)

        else:
            print(f"no se ha encontrado el usuario con dni {dni}")

    def consultas_estadisticas(self) -> None:
        """
        Funcion que inicializa el menu de funciones para las consultas y estadisticas
        :return: None
        """

        opciones_consultas = {
            1: self.listar_personas_existentes,
            2: self.listar_n_mejores,
            3: self.listar_n_mejores_categoria,
            4: self.listar_n_mejores_calorias,
            5: self.listar_n_mejores_monitores
        }

        self._ejecutar_menu(ZaidinGym.menu_consultas_estadisticas, opciones_consultas, 6)

    """
    -----------------------------
    GESTION DE USUARIOS
    -----------------------------
    """

    def alta_persona(self)->None:
        """
        Funcion que da de alta una persona.\n

        Primeramente, se piden los datos del usuario compartidos entre todos los tipos, y posteriormente se piden los datos
        de cada tipo de usuario según el tipo de usuario que se quiera crear.\n

        Si se crea el usuario se mete automaticamente en la lista de usuarios.
        :return: None
        """

        nombre = input("Ingrese el nombre: ").strip()
        dni = input("Ingrese el DNI: ").strip()
        direccion = input("Ingrese la direccion: ").strip()
        provincia = input("Ingrese la provincia: ").strip()
        codigo_postal = input("Ingrese el codigo postal: ").strip()
        telefono = input("Ingrese el telefono: ").strip()

        fecha_nacimiento = self._pedir_fecha("Ingrese la fecha de nacimiento (dd/mm/aaaa): ")

        opcion = 0

        while opcion not in [1,2,3]:
            print("Que tipo de usuario quiere dar de alta.\n"
                  "1. Monitor\n"
                  "2. Socio\n"
                  "3. Socio Premium\n")

            try:
                opcion = int(input("Ingrese el tipo de usuario: "))
            except ValueError:
                print("Introduce una opcion correcta")
                continue

            if opcion == 1:
                print(f"Especialidades: ", ", ".join(esp.name for esp in Especialidad))
                especialidades = self._pedir_especialidad()

                sueldo = float(input("Ingrese el sueldo: "))
                votos_positivos = int(input("Introduce los votos positivos: "))
                votos_negativos = int(input("Introduce los votos negativos: "))

                especialiades_enum = [Especialidad(e) for e in especialidades]


                try:
                    monitor = Monitor(nombre, dni, direccion, provincia, codigo_postal, telefono, fecha_nacimiento, especialiades_enum,
                            sueldo, votos_positivos, votos_negativos)
                    self.__lista_usuarios.append(monitor)
                    print("Monitor creado con exito")
                except ValueError:
                    print("Error al crear el monitor")

            if opcion == 2:
                fecha_registro = self._pedir_fecha("Ingrese la fecha de registro (dd/mm/aaaa)")
                fecha_ultimo_acceso = self._pedir_fecha("Ingrese la ultima fecha de acceso (dd/mm/aaaa)")
                esta_activo = self._pedir_boolean("Introduce si se encuentra activo en la plataforma (s/n)")
                print(f"Lista de actividades disponibles: ", ", ".join(a.nombre for a in self.__lista_actividades))
                lista_actividades = self._comprobar_lista_actividades()

                try:
                    socio = Socio(nombre, dni, direccion, provincia, codigo_postal, telefono, fecha_nacimiento, fecha_registro,
                                  fecha_ultimo_acceso, esta_activo, lista_actividades)

                    self.__lista_usuarios.append(socio)
                    print("Socio creado con exito")
                except ValueError:
                    print("Error al crear el socio")

            if opcion == 3:
                fecha_registro = self._pedir_fecha("Ingrese la fecha de registro (dd/mm/aaaa)")
                fecha_ultimo_acceso = self._pedir_fecha("Ingrese la ultima fecha de acceso (dd/mm/aaaa)")
                esta_activo = self._pedir_boolean("Introduce si se encuentra activo en la plataforma (s/n)")
                print(f"Lista de actividades disponibles: ", ", ".join(a.nombre for a in self.__lista_actividades))
                lista_actividades = self._comprobar_lista_actividades()
                es_premium = True

                try:
                    socio = SocioPremium(nombre, dni, direccion, provincia, codigo_postal, telefono, fecha_nacimiento,
                                  fecha_registro,fecha_ultimo_acceso, esta_activo, lista_actividades, es_premium)

                    self.__lista_usuarios.append(socio)
                    print("Socio creado con exito")
                except ValueError:
                    print("Error al crear el socio")

    def baja_persona(self)->None:
        """
        Funcion que elimina un usuario de la plataforma.\n

        Si se encuentra el usuario pregunta si se quiere eliminar
        :return: None
        """
        dni = input("Introduce el dni de la persona que quiere eliminar: ")
        persona = self._buscar_persona_dni(dni)

        if persona:
            print("¿Esta seguro de eliminar este usuario?")
            print(persona)
            respuesta = self._pedir_boolean("¿Eliminar este usuario? (s/n): ")

            if respuesta:
                self.__lista_usuarios.remove(persona)
            else:
                print("Cancelado.")
        else:
            print(f"No se ha encontrado el usuario con el dni {dni}")

    def gestionar_monitores(self, nombre:str)->None:
        """
        Funcion que ejecuta una serie de funciones auxiliares para actualizar el sueldo, actualizar las especialidaddes
        y valorar el monitor
        :param nombre: String con el nombre del monitor
        :return: None
        """

        nombre_str = nombre.lower().strip()
        encontrado = False

        for monitor in self.__lista_usuarios:
            if monitor.nombre.strip().lower() == nombre_str:
                encontrado = True
                print(monitor)

                opciones_monitor = {
                    1: lambda :self._actualizar_sueldo(monitor),
                    2: lambda :self._actualizar_especialidades(monitor),
                    3: lambda :self._valorar_monitor(monitor),
                }

                self._ejecutar_menu(ZaidinGym.menu_gestion_monitor, opciones_monitor, 4)
                break

        if not encontrado:
            print(f"No se ha encontrado el monitor {nombre}")

    def inactivar_socios(self):
        """
        Función que inactiva todos los usuarios que no se han
        :return: None
        """

        hoy = date.today()
        un_mes = hoy - timedelta(days=30)
        for usuario in self.__lista_usuarios:
            if isinstance(usuario, (Socio, SocioPremium)):
                if usuario.fecha_ultimo_acceso < un_mes and usuario.esta_activo:
                    usuario.esta_activo = False
                    print(f"{usuario.nombre} ha sido inactivado")

    """
    ---------------------------
    GESTION DE SOCIOS
    ---------------------------
    """

    @staticmethod
    def mostrar_lista_actividades(socio:Socio | SocioPremium)->None:
        """
        Funcion que muestra la lista de actividades de un socio
        :param socio: Socio | SocioPremium objeto con la lista de actividades
        :return: None
        """
        if isinstance(socio, Socio):

            if len(socio.lista_actividades) ==0:
                print("La lista de actividades esta vacía")
            else:
                print(f"Duracion de la lista de actividades: {socio.get_duracion_actividades()/60} horas")
                for actividad in socio.lista_actividades:
                    print(actividad)

        else:
            print("Los monitores no tienen lista de actividades")

    def nueva_actividad_lista(self, socio:Socio | SocioPremium)->None:
        """
        Funcion que añade una actividad nueva a la lista del socio pasado por parametro siempre y cuando sea posible
        :param socio: Socio | SocioPremium con la lista de actividades
        :return: None
        """
        print("Lista de actividades")
        for actividad in self.__lista_actividades:
            print(actividad)

        nombre = input("Introduce el nombre de la actividad que quieres añadir: ")

        for actividad in self.__lista_actividades:
            if actividad.nombre == nombre:
                try:
                    socio.add_actividad(actividad)
                    print(f"{actividad.nombre} agregada correctamente")
                except ValueError as e:
                    print(f"Error al añadir la actividad a la lista de actividades: {e}")
            else:
                print(f"El nombre {nombre} no esta en la lista de actividades")

    def eliminar_actividad_lista(self)->None:
        raise NotImplementedError

    def valorar_actividad(self) -> None:
        raise NotImplementedError

    def convertir_premium(self) -> None:
        raise NotImplementedError

    """
    ---------------------------
    GESTION DE ACTIVIDADES (CREAR Y ELIMINAR)
    ---------------------------
    """

    def nueva_actividad(self)->None:
        """
        Funcion que crea una nueva actividad del gimnasio.\n

        Si se ha creado la actividad se agrega automaticamente a la lista de actividades
        :return: None
        """

        nombre = input("Ingrese el nombre de la actividad: ")
        duracion = int(input("Ingrese la duracion de la actividad en minutos: "))
        calorias = int(input("Ingrese las calorias de la actividad: "))
        print("Las categorias validas son: ", ", ".join(e.name for e in Especialidad))
        categoria = self._pedir_categoria_actividad()
        es_premium = self._pedir_boolean("Introduce si la actividad es premium (s/n)")

        try:
            actividad = Actividad(nombre, duracion, calorias, categoria, es_premium)

            for act in self.__lista_actividades:
                if act == actividad:
                    print("Ya hay una actividad igual creada")
                    return

            self.__lista_usuarios.append(actividad)
            print("Actividad creada con exito")

        except ValueError:
            print("Error al crear el actividad")

    def eliminar_actividad(self, nombre:str)->None:
        """
        Función que elimina una actividad del gimnasio.\n

        Si la actividad está seleccionada por algún socio no se elimina y muestra todos los socios que tienen esa actividad.
        :param nombre: Str con el nombre de la actividad
        :return: None
        """
        nombre = nombre.lower()

        for usuario in self.__lista_usuarios:
            for actividad in usuario.lista_actividades:
                if actividad.nombre == nombre:
                    print("No se puede eliminar esta actividad, hay un usuario que tiene esta actividad seleccionada.")
                    socios_actividad = self._listar_personas_actividad(nombre)
                    for socio in socios_actividad:
                        print(socio)

                    return

        for actividad in self.__lista_actividades:
            if actividad.nombre == nombre:
                self.__lista_usuarios.remove(actividad)
                print("Actividad eliminada con exito")

    """
    -----------------------------
    CONSULTAS Y ESTADISTICAS
    ------------------------------
    """

    def listar_personas_existentes(self):
        raise NotImplementedError

    def listar_n_mejores(self):
        raise NotImplementedError

    def listar_n_mejores_categoria(self):
        raise NotImplementedError

    def listar_n_mejores_calorias(self):
        raise NotImplementedError

    def listar_n_mejores_monitores(self):
        raise NotImplementedError

    """
    ------------------------------
        FUNCIONES AUXILIARES
    ------------------------------
    """

    @staticmethod
    def _ejecutar_menu(menu_func: Callable[[], None],opciones: dict,opcion_salida: int) -> None:
        """
        Funcion que valida la entrada de datos en los menús para evitar la duplicidad y ejecuta la accion correspondiente
        :param menu_func:Callable [] con menu que contiene las opciones válidas, devuelve None
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
    def _pedir_categoria_actividad()->Especialidad:
        """
        Funcion auxiliar que devuelve la categoria de la actividad correcta según el Enum de Especialidad
        :return: Especialidad con el name y value de la categoria de la actividad
        """
        while True:
            entrada = input("Introduce la categoria de la actividad: ").strip().lower()

            try:
                return Especialidad(entrada)
            except ValueError:
                print("Categoria no válida")
                print("Las categorias validas son:", ", ".join(e.value for e in Especialidad))

    @staticmethod
    def _pedir_especialidad() -> list[str]:
        """
        Funcion auxiliar que pide al usuario una lista de especialidades separadas por comas, valída que existe en
        Especialidad y devuelve un list de strings
        :return: list[str] con las especialidades
        """

        while True:
            entrada = input("Ingrese las especialidades separadas por comas: ")
            lista = [esp.strip().lower() for esp in entrada.split(",") if esp.strip()]

            invalidas = [esp for esp in lista if esp not in [e.value for e in Especialidad]]

            if invalidas:
                print("Especialidades invalidadas: ", ", ".join(invalidas))
                print("Las especialidades validas son: ", ", ".join(e.value for e in Especialidad))
            else:
                return lista

    def _comprobar_lista_actividades(self)->list[Actividad]:
        """
        Función auxiliar que agrega a una lista las actividades cuyos nombres ha introducido el usuario por teclado
        separadas por comas
        :return: list[Actividad] con las actividades que ha seleccionado el usuario
        """
        while True:
            entrada = input("Introduce el nombre de las actividades separadas por comas: ")
            nombres = [act.strip().lower() for act in entrada.split(",") if act.strip()]
            actividades_seleccionadas = []
            invalidas = []

            for nombre in nombres:
                encontrada = None

                for actividad in self.__lista_actividades:
                    if actividad.nombre.lower() == nombre:
                        encontrada = actividad
                        break

                if encontrada:
                    actividades_seleccionadas.append(encontrada)
                else:
                    invalidas.append(nombre)

            if invalidas:
                print("Actividades invalidas:", ", ".join(invalidas))
                print("Actividades validas:", ", ".join(a.nombre for a in self.__lista_actividades))
            else:
                return actividades_seleccionadas

    @staticmethod
    def _pedir_fecha(mensaje:str) -> date:
        """
        Funcion auxiliar que devuelve una fecha de formato dd/mm/aaaa a un datetime
        :param mensaje: str con la fecha dd/mm/aaaa
        :return: datetime
        """
        while True:
            fecha_str = input(mensaje).strip()

            try:
                return datetime.strptime(fecha_str, "%d/%m/%Y").date()
            except ValueError:
                print("Formato incorrecto. Usa dd/mm/aaaa")

    @staticmethod
    def _pedir_boolean(mensaje:str) -> bool:
        """
        Funcion auxiliar que devuelve un bool transformando un (s/n)
        :param mensaje: str con el valor que se quiere transformar
        :return:
        """
        while True:
            activo = input(mensaje).strip()

            if activo in ["s", "n"]:
                if activo == "s":
                    return True
                else:
                    return False
            else:
                print("Introduce un valor correcto (s/n)")

    def _listar_personas_actividad(self, nombre_actividad:str)->list[Socio | SocioPremium]:
        """
        Funcion auxiliar que busca los socios que tengan en su lista de actividades una actividad con el nombre pasado
        por parametro
        :param nombre_actividad: str con el nombre de la actividad
        :return: list[Socio | SocioPremium] con los socios que tengan en su lista la actividad
        """

        nombre_actividad = nombre_actividad.strip().lower()
        lista_usuarios = []

        for usuario in self.__lista_usuarios:
            for actividad in usuario.lista_actividades:
                if actividad == nombre_actividad:
                    lista_usuarios.append(usuario)

        return lista_usuarios

    @staticmethod
    def _actualizar_sueldo(monitor:Monitor)->None:
        """
        Funcion auxiliar de gestionar monitores que actualiza el sueldo de un monitor cuyo nombre se pasa por parametro
        :param monitor: Monitor objeto a actualizar
        :return: None
        """
        while True:
            nuevo_sueldo = float(input("Introduce el nuevo sueldo (minimo 1184€): ").strip())

            try:
                monitor.sueldo = nuevo_sueldo
            except ValueError as e:
                print(f"Error al actualizar el sueldo {e}")

    def _actualizar_especialidades(self, monitor:Monitor)->None:
        """
        Funcion auxiliar de gestionar monitores que actualiza la lista de especialidades del monitor que se pasa por parametro
        :param monitor: Monitor objeto a actualizar
        :return: None
        """

        print("Especialidades del monitor")
        for esp in monitor.especialidad:
            print(esp)

        print("Introduzca de nuevo las especialidades del monitor")
        especialidades = self._pedir_especialidad()

        especialiades_enum = [Especialidad(e) for e in especialidades]
        try:
            monitor.especialidad = especialiades_enum
        except ValueError as e:
            print(f"Error al actualizar el especialidad {e}")

    def _valorar_monitor(self, monitor:Monitor)->None:
        """
        Funcion auxiliar de gestionar monitores la cual valora positivamente o negativamente a un monitor
        :param monitor: Monitor objeto a actualizar
        :return: None
        """
        like = self._pedir_boolean("Para valorar positivamente introduce 's', para valorarlo negativamente introduce 'n')")

        monitor.me_gusta(like)
        print("¡Gracias por valorar!")

    def _buscar_persona_dni(self, dni:str)->Socio | SocioPremium | Monitor |None:
        """
        Funcion auxiliar que devuelve un Socio | SocioPremium | Monitor si el dni pasado por parametro está asociado a un usuario
        :param dni: String con el dni del usuario
        :return: Socio | SocioPremium | Monitor | None
        """

        for usuario in self.__lista_usuarios:
            if isinstance(usuario, (Socio, SocioPremium, Monitor)):
                if usuario.dni == dni:
                    return usuario
        return None

    """
    --------------------------
            MENUS
    --------------------------
    """

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
    def menu_consultas_estadisticas():
        print("\n1. Listar personas existentes")
        print("2. Listar las n mejores actividades")
        print("3. Listar las n mejores actividades por categoria")
        print("4. Listar las n mejores actividades por cantidad de kcal")
        print("5. Listar los n mejores monitores")
        print("6. Volver")

    @staticmethod
    def menu_actividades():
        print("1. Nueva actividad")
        print("2. Eliminar actividad")
        print("3. Volver")

    @staticmethod
    def menu_gestion_monitor():
        print("1. Actualizar sueldo")
        print("2. Actualizar lista de especialidades")
        print("3. Realizar una valoracion")
        print("4. Volver")

if __name__ == "__main__":
    gym = ZaidinGym()
    gym.main()