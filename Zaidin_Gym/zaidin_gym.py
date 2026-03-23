from datetime import datetime, date
from typing import Callable

from Class.actividad import Actividad
from Class.especialidad import Especialidad
from Class.monitor import Monitor
from Class.socio import Socio
from Class.socio_premium import SocioPremium
from Database.database import init_db, get_session
from Database import repository as repo


class ZaidinGym:

    def __init__(self):
        # Inicializar la base de datos (crea tablas si no existen)
        init_db()
        self.__session = get_session()

        # Cargar datos de prueba solo si la BD está vacía
        if not self.__session.query(__import__('Database.models', fromlist=['UsuarioModel']).UsuarioModel).first():
            self._cargar_datos_prueba()

    """
    -----------------------------------
                MAIN
    -----------------------------------
    """

    def main(self) -> None:
        print("Bienvenido a ZaidinGym")
        opcion = 0

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
                print("Saliendo del programa")
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
        opciones_actividades = {
            1: self.nueva_actividad,
            2: self.eliminar_actividad,
        }
        self._ejecutar_menu(ZaidinGym.menu_actividades, opciones_actividades, 3)

    def gestionar_usuarios(self) -> None:
        opciones_usuarios = {
            1: self.alta_persona,
            2: self.baja_persona,
            3: self.gestionar_socios,
            4: self.gestionar_monitores,
            5: self.inactivar_socios
        }
        self._ejecutar_menu(ZaidinGym.menu_gestion_usuarios, opciones_usuarios, 6)

    def gestionar_socios(self) -> None:
        dni = input("Introduce el DNI del socio: ").strip()
        persona = repo.obtener_usuario_por_dni(self.__session, dni)

        if persona is None:
            print(f"No se ha encontrado el usuario con DNI {dni}")
            return

        if isinstance(persona, Monitor):
            print("El DNI introducido corresponde a un monitor, no a un socio")
            return

        repo.actualizar_fecha_ultimo_acceso(self.__session, dni, date.today())
        persona.fecha_ultimo_acceso = date.today()

        if isinstance(persona, SocioPremium):
            opciones_socios = {
                1: lambda: self.mostrar_lista_actividades(persona),
                2: lambda: self.nueva_actividad_lista(persona, dni),
                3: lambda: self.eliminar_actividad_lista(persona, dni),
                4: lambda: self.valorar_actividad(persona),
            }
            self._ejecutar_menu(ZaidinGym.menu_gestion_socios_premium, opciones_socios, 5)
        else:
            opciones_socios = {
                1: lambda: self.mostrar_lista_actividades(persona),
                2: lambda: self.nueva_actividad_lista(persona, dni),
                3: lambda: self.eliminar_actividad_lista(persona, dni),
                4: lambda: self.valorar_actividad(persona),
                5: lambda: self.convertir_premium(persona, dni),
            }
            self._ejecutar_menu(ZaidinGym.menu_gestion_socios, opciones_socios, 6)

    def consultas_estadisticas(self) -> None:
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

    def alta_persona(self) -> None:
        nombre = input("Ingrese el nombre: ").strip()
        dni = input("Ingrese el DNI: ").strip()
        direccion = input("Ingrese la direccion: ").strip()
        provincia = input("Ingrese la provincia: ").strip()
        codigo_postal = input("Ingrese el codigo postal: ").strip()
        telefono = input("Ingrese el telefono: ").strip()
        fecha_nacimiento = self._pedir_fecha("Ingrese la fecha de nacimiento (dd/mm/aaaa): ")

        opcion = 0
        while opcion not in [1, 2, 3]:
            print("Que tipo de usuario quiere dar de alta.\n"
                  "1. Monitor\n2. Socio\n3. Socio Premium\n")
            try:
                opcion = int(input("Ingrese el tipo de usuario: "))
            except ValueError:
                print("Introduce una opcion correcta")
                continue

            if opcion == 1:
                print("Especialidades: ", ", ".join(esp.name for esp in Especialidad))
                especialidades = self._pedir_especialidad()
                sueldo = float(input("Ingrese el sueldo: "))
                votos_positivos = int(input("Introduce los votos positivos: "))
                votos_negativos = int(input("Introduce los votos negativos: "))
                especialidades_enum = [Especialidad(e) for e in especialidades]
                try:
                    monitor = Monitor(nombre, dni, direccion, provincia, codigo_postal, telefono,
                                      fecha_nacimiento, especialidades_enum, sueldo, votos_positivos, votos_negativos)
                    repo.crear_monitor(self.__session, monitor)
                    print("Monitor creado con exito")
                except (ValueError, TypeError) as e:
                    print(f"Error al crear el monitor: {e}")

            elif opcion == 2:
                fecha_registro = self._pedir_fecha("Ingrese la fecha de registro (dd/mm/aaaa): ")
                fecha_ultimo_acceso = self._pedir_fecha("Ingrese la ultima fecha de acceso (dd/mm/aaaa): ")
                esta_activo = self._pedir_boolean("Introduce si se encuentra activo (s/n): ")
                actividades_disponibles = repo.obtener_actividades(self.__session)
                print("Actividades disponibles: ", ", ".join(a.nombre for a in actividades_disponibles))
                lista_actividades = self._seleccionar_actividades(actividades_disponibles)
                try:
                    socio = Socio(nombre, dni, direccion, provincia, codigo_postal, telefono,
                                  fecha_nacimiento, fecha_registro, fecha_ultimo_acceso, esta_activo, lista_actividades)
                    repo.crear_socio(self.__session, socio)
                    print("Socio creado con exito")
                except (ValueError, TypeError) as e:
                    print(f"Error al crear el socio: {e}")

            elif opcion == 3:
                fecha_registro = self._pedir_fecha("Ingrese la fecha de registro (dd/mm/aaaa): ")
                fecha_ultimo_acceso = self._pedir_fecha("Ingrese la ultima fecha de acceso (dd/mm/aaaa): ")
                esta_activo = self._pedir_boolean("Introduce si se encuentra activo (s/n): ")
                actividades_disponibles = repo.obtener_actividades(self.__session)
                print("Actividades disponibles: ", ", ".join(a.nombre for a in actividades_disponibles))
                lista_actividades = self._seleccionar_actividades(actividades_disponibles)
                try:
                    socio = SocioPremium(nombre, dni, direccion, provincia, codigo_postal, telefono,
                                         fecha_nacimiento, fecha_registro, fecha_ultimo_acceso,
                                         esta_activo, lista_actividades, True)
                    repo.crear_socio_premium(self.__session, socio)
                    print("Socio Premium creado con exito")
                except (ValueError, TypeError) as e:
                    print(f"Error al crear el socio premium: {e}")

    def baja_persona(self) -> None:
        dni = input("Introduce el DNI de la persona que quiere eliminar: ").strip()
        persona = repo.obtener_usuario_por_dni(self.__session, dni)

        if persona:
            print(persona)
            respuesta = self._pedir_boolean("¿Eliminar este usuario? (s/n): ")
            if respuesta:
                repo.eliminar_usuario(self.__session, dni)
                print("Usuario eliminado correctamente")
            else:
                print("Cancelado.")
        else:
            print(f"No se ha encontrado el usuario con DNI {dni}")

    def gestionar_monitores(self) -> None:
        nombre = input("Introduce el nombre del monitor: ").strip()
        persona = repo.obtener_usuario_por_nombre(self.__session, nombre)

        if persona is None or not isinstance(persona, Monitor):
            print(f"No se ha encontrado el monitor {nombre}")
            return

        print(persona)
        opciones_monitor = {
            1: lambda: self._actualizar_sueldo(persona, nombre),
            2: lambda: self._actualizar_especialidades(persona, nombre),
            3: lambda: self._valorar_monitor(nombre),
        }
        self._ejecutar_menu(ZaidinGym.menu_gestion_monitor, opciones_monitor, 4)

    def inactivar_socios(self) -> None:
        nombres = repo.inactivar_socios_antiguos(self.__session, dias=30)
        if nombres:
            for nombre in nombres:
                print(f"{nombre} ha sido inactivado")
        else:
            print("No hay socios que inactivar")

    """
    ---------------------------
    GESTION DE SOCIOS
    ---------------------------
    """

    @staticmethod
    def mostrar_lista_actividades(socio: Socio | SocioPremium) -> None:
        if isinstance(socio, Socio):
            if not socio.lista_actividades:
                print("La lista de actividades esta vacía")
            else:
                print(f"Duracion total: {socio.get_duracion_actividades()} minutos")
                for actividad in socio.lista_actividades:
                    print(actividad)
        else:
            print("Los monitores no tienen lista de actividades")

    def nueva_actividad_lista(self, socio: Socio | SocioPremium, dni: str) -> None:
        actividades = repo.obtener_actividades(self.__session)
        print("Lista de actividades disponibles:")
        for actividad in actividades:
            print(f"  - {actividad.nombre}")

        nombre = input("Introduce el nombre de la actividad que quieres añadir: ").strip()

        encontrada = next((a for a in actividades if a.nombre.lower() == nombre.lower()), None)

        if encontrada:
            try:
                socio.add_actividad(encontrada)
                repo.añadir_actividad_socio(self.__session, dni, encontrada.nombre)
                print(f"{encontrada.nombre} agregada correctamente")
            except ValueError as e:
                print(f"Error al añadir la actividad: {e}")
        else:
            print(f"No se encontró la actividad '{nombre}'")

    def eliminar_actividad_lista(self, socio: Socio | SocioPremium, dni: str) -> None:
        print("Lista de actividades del socio:")
        for actividad in socio.lista_actividades:
            print(f"  - {actividad.nombre}")

        nombre = input("Escribe el nombre de la actividad que quieres eliminar: ").strip()
        encontrada = next((a for a in socio.lista_actividades if a.nombre.lower() == nombre.lower()), None)

        if encontrada:
            try:
                socio.del_actividad(encontrada)
                repo.eliminar_actividad_socio(self.__session, dni, encontrada.nombre)
                print(f"Actividad {encontrada.nombre} eliminada correctamente")
            except ValueError as e:
                print(f"Error al eliminar la actividad: {e}")
        else:
            print(f"No se ha encontrado la actividad '{nombre}'")

    def valorar_actividad(self, socio: Socio | SocioPremium) -> None:
        print("¿Qué actividad quiere valorar?")
        for actividad in socio.lista_actividades:
            print(f"  - {actividad.nombre}")

        nombre = input("Introduce el nombre de la actividad: ").strip()
        encontrada = next((a for a in socio.lista_actividades if a.nombre.lower() == nombre.lower()), None)

        if encontrada:
            try:
                nota = int(input("Introduce la nota (0-10): "))
                if encontrada.votar(nota):
                    repo.votar_actividad(self.__session, encontrada.nombre, nota)
                    print("Gracias por valorar")
                else:
                    print("La nota debe estar entre 0 y 10")
            except ValueError as e:
                print(f"Error al valorar: {e}")
        else:
            print(f"No se encontró la actividad '{nombre}'")

    def convertir_premium(self, socio: Socio, dni: str) -> None:
        if isinstance(socio, Socio) and not isinstance(socio, SocioPremium):
            if repo.convertir_socio_a_premium(self.__session, dni):
                print(f"{socio.nombre} convertido a socio premium correctamente")
            else:
                print("No se pudo convertir el socio a premium")

    """
    ---------------------------
    GESTION DE ACTIVIDADES
    ---------------------------
    """

    def nueva_actividad(self) -> None:
        nombre = input("Ingrese el nombre de la actividad: ").strip()
        duracion = int(input("Ingrese la duracion en minutos: "))
        calorias = int(input("Ingrese las calorias: "))
        print("Categorias validas: ", ", ".join(e.value for e in Especialidad))
        categoria = self._pedir_categoria_actividad()
        es_premium = self._pedir_boolean("¿Es actividad premium? (s/n): ")

        try:
            actividad = Actividad(nombre, duracion, calorias, categoria, es_premium)
            existente = repo.obtener_actividad_por_nombre(self.__session, nombre)
            if existente:
                print("Ya existe una actividad con ese nombre")
                return
            repo.crear_actividad(self.__session, actividad)
            print("Actividad creada con exito")
        except (ValueError, TypeError) as e:
            print(f"Error al crear la actividad: {e}")

    def eliminar_actividad(self) -> None:
        nombre = input("Introduce el nombre de la actividad a eliminar: ").strip()

        socios_con_actividad = repo.actividad_tiene_socios(self.__session, nombre)
        if socios_con_actividad:
            print("No se puede eliminar esta actividad. La tienen los siguientes socios:")
            for s in socios_con_actividad:
                print(f"  - {s}")
            return

        if repo.eliminar_actividad(self.__session, nombre):
            print("Actividad eliminada con exito")
        else:
            print(f"No se encontró la actividad '{nombre}'")

    """
    -----------------------------
    CONSULTAS Y ESTADISTICAS
    ------------------------------
    """

    def listar_personas_existentes(self) -> None:
        opciones_lista = {
            1: self._listar_todos,
            2: self._listar_monitores,
            3: self._listar_socios,
            4: self._listar_socios_premium
        }
        self._ejecutar_menu(ZaidinGym.menu_listar_personas, opciones_lista, 5)

    def listar_n_mejores(self) -> None:
        try:
            numero = int(input("Introduce el numero de actividades que quieres mostrar: "))
            actividades = repo.obtener_actividades(self.__session)
            ordenadas = sorted(actividades, key=lambda a: a.calcular_valoracion(), reverse=True)
            for actividad in ordenadas[:numero]:
                print(actividad)
        except ValueError:
            print("Introduce un valor correcto")

    def listar_n_mejores_categoria(self) -> None:
        try:
            numero = int(input("Introduce el numero de actividades que quieres mostrar: "))
            print("Categorias: ", ", ".join(e.value for e in Especialidad))
            categoria = self._pedir_categoria_actividad()
            actividades = repo.obtener_actividades(self.__session)
            filtradas = [a for a in actividades if a.categoria == categoria]
            ordenadas = sorted(filtradas, key=lambda a: a.calcular_valoracion(), reverse=True)
            for actividad in ordenadas[:numero]:
                print(actividad)
        except ValueError:
            print("Introduce un valor correcto")

    def listar_n_mejores_calorias(self) -> None:
        try:
            numero = int(input("Introduce el numero de actividades que quieres mostrar: "))
            actividades = repo.obtener_actividades(self.__session)
            ordenadas = sorted(actividades, key=lambda a: a.calorias, reverse=True)
            for actividad in ordenadas[:numero]:
                print(actividad)
        except ValueError:
            print("Introduce un valor correcto")

    def listar_n_mejores_monitores(self) -> None:
        try:
            numero = int(input("Introduce el numero de monitores que quieres mostrar: "))
            usuarios = repo.obtener_usuarios(self.__session)
            monitores = [u for u in usuarios if isinstance(u, Monitor)]
            ordenados = sorted(monitores, key=lambda m: m.calcular_valoracion(), reverse=True)
            for monitor in ordenados[:numero]:
                print(monitor)
        except ValueError:
            print("Introduce un valor correcto")

    """
    ------------------------------
        FUNCIONES AUXILIARES
    ------------------------------
    """

    def _listar_todos(self) -> None:
        print("Todos los usuarios:")
        for usuario in repo.obtener_usuarios(self.__session):
            print(usuario)

    def _listar_monitores(self) -> None:
        print("Monitores:")
        for usuario in repo.obtener_usuarios(self.__session):
            if isinstance(usuario, Monitor):
                print(usuario)

    def _listar_socios(self) -> None:
        print("Socios:")
        for usuario in repo.obtener_usuarios(self.__session):
            if isinstance(usuario, Socio) and not isinstance(usuario, SocioPremium):
                print(usuario)

    def _listar_socios_premium(self) -> None:
        print("Socios premium:")
        for usuario in repo.obtener_usuarios(self.__session):
            if isinstance(usuario, SocioPremium):
                print(usuario)

    def _actualizar_sueldo(self, monitor: Monitor, nombre: str) -> None:
        while True:
            try:
                nuevo_sueldo = float(input("Introduce el nuevo sueldo (minimo 1184€): ").strip())
                monitor.sueldo = nuevo_sueldo
                repo.actualizar_sueldo_monitor(self.__session, nombre, nuevo_sueldo)
                print("Sueldo actualizado correctamente")
                break
            except (ValueError, TypeError) as e:
                print(f"Error al actualizar el sueldo: {e}")

    def _actualizar_especialidades(self, monitor: Monitor, nombre: str) -> None:
        print("Especialidades actuales:")
        for esp in monitor.especialidad:
            print(f"  - {esp.value}")

        especialidades = self._pedir_especialidad()
        especialidades_enum = [Especialidad(e) for e in especialidades]
        try:
            monitor.especialidad = especialidades_enum
            repo.actualizar_especialidades_monitor(self.__session, nombre, especialidades_enum)
            print("Especialidades actualizadas correctamente")
        except ValueError as e:
            print(f"Error al actualizar especialidades: {e}")

    def _valorar_monitor(self, nombre: str) -> None:
        like = self._pedir_boolean("Para valorar positivamente introduce 's', negativamente 'n': ")
        repo.votar_monitor(self.__session, nombre, like)
        print("¡Gracias por valorar!")

    @staticmethod
    def _seleccionar_actividades(actividades_disponibles: list[Actividad]) -> list[Actividad]:
        while True:
            entrada = input("Introduce el nombre de las actividades separadas por comas (o pulsa Enter para ninguna): ").strip()
            if not entrada:
                return []

            nombres = [n.strip().lower() for n in entrada.split(",") if n.strip()]
            seleccionadas = []
            invalidas = []

            for nombre in nombres:
                encontrada = next((a for a in actividades_disponibles if a.nombre.lower() == nombre), None)
                if encontrada:
                    seleccionadas.append(encontrada)
                else:
                    invalidas.append(nombre)

            if invalidas:
                print("Actividades no encontradas:", ", ".join(invalidas))
                print("Disponibles:", ", ".join(a.nombre for a in actividades_disponibles))
            else:
                return seleccionadas

    @staticmethod
    def _ejecutar_menu(menu_func: Callable[[], None], opciones: dict, opcion_salida: int) -> None:
        opcion = 0
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
    def _pedir_categoria_actividad() -> Especialidad:
        while True:
            entrada = input("Introduce la categoria: ").strip().lower()
            try:
                return Especialidad(entrada)
            except ValueError:
                print("Categoria no válida. Validas:", ", ".join(e.value for e in Especialidad))

    @staticmethod
    def _pedir_especialidad() -> list[str]:
        while True:
            entrada = input("Ingrese las especialidades separadas por comas: ")
            lista = [esp.strip().lower() for esp in entrada.split(",") if esp.strip()]
            invalidas = [esp for esp in lista if esp not in [e.value for e in Especialidad]]
            if invalidas:
                print("Especialidades invalidas:", ", ".join(invalidas))
                print("Validas:", ", ".join(e.value for e in Especialidad))
            else:
                return lista

    @staticmethod
    def _pedir_fecha(mensaje: str) -> date:
        while True:
            fecha_str = input(mensaje).strip()
            try:
                return datetime.strptime(fecha_str, "%d/%m/%Y").date()
            except ValueError:
                print("Formato incorrecto. Usa dd/mm/aaaa")

    @staticmethod
    def _pedir_boolean(mensaje: str) -> bool:
        while True:
            activo = input(mensaje).strip().lower()
            if activo == "s":
                return True
            elif activo == "n":
                return False
            else:
                print("Introduce un valor correcto (s/n)")

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
        print("\n1. Alta personas (socios o monitores)")
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
    def menu_gestion_socios_premium():
        print("\n1. Mostrar lista de actividades")
        print("2. Añadir actividad")
        print("3. Eliminar actividad")
        print("4. Valorar actividad")
        print("5. Volver")

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
        print("\n1. Nueva actividad")
        print("2. Eliminar actividad")
        print("3. Volver")

    @staticmethod
    def menu_gestion_monitor():
        print("\n1. Actualizar sueldo")
        print("2. Actualizar lista de especialidades")
        print("3. Realizar una valoracion")
        print("4. Volver")

    @staticmethod
    def menu_listar_personas():
        print("\n1. Listar todos los usuarios")
        print("2. Listar solo los monitores")
        print("3. Listar solo los socios")
        print("4. Listar solo los socios premium")
        print("5. Volver")

    """
    --------------------------
        DATOS DE PRUEBA
    --------------------------
    """

    def _cargar_datos_prueba(self):
        from Database import repository as repo

        a1 = Actividad("Yoga Matutino",     60,  250, Especialidad.CORE,     False)
        a2 = Actividad("Spinning Extremo",  45,  500, Especialidad.CICLISMO, False)
        a3 = Actividad("Baile Latino",      60,  400, Especialidad.BAILE,    False)
        a4 = Actividad("HIIT Avanzado",     30,  600, Especialidad.HIIT,     True)
        a5 = Actividad("Natacion Premium",  90,  350, Especialidad.PISCINA,  True)
        a6 = Actividad("Cardio Total",      45,  480, Especialidad.CARDIO,   False)
        a7 = Actividad("Body Stretching",   60,  200, Especialidad.BODYCARE, False)
        a8 = Actividad("Fitness Funcional", 50,  550, Especialidad.FITNESS,  True)

        a1.votar(8); a1.votar(9); a1.votar(7)
        a2.votar(6); a2.votar(7); a2.votar(8)
        a3.votar(9); a3.votar(10); a3.votar(9)
        a4.votar(5); a4.votar(6)
        a5.votar(10); a5.votar(9); a5.votar(10)
        a6.votar(7); a6.votar(8)
        a7.votar(4); a7.votar(5)
        a8.votar(8); a8.votar(9); a8.votar(10)

        for actividad in [a1, a2, a3, a4, a5, a6, a7, a8]:
            repo.crear_actividad(self.__session, actividad)

        m1 = Monitor("Carlos Garcia Lopez", "12345678Z", "Calle Mayor 1", "Granada", "18001",
                     "600111222", date(1985, 3, 15), [Especialidad.FITNESS, Especialidad.HIIT], 1500.0, 20, 3)
        m2 = Monitor("Ana Martinez Ruiz", "87654321X", "Avenida Constitucion 5", "Granada", "18002",
                     "600333444", date(1990, 7, 22), [Especialidad.BAILE, Especialidad.CARDIO, Especialidad.CORE], 1800.0, 35, 2)
        m3 = Monitor("Pedro Sanchez Mora", "11223344B", "Plaza Nueva 10", "Granada", "18003",
                     "600555666", date(1988, 11, 5), [Especialidad.PISCINA, Especialidad.CICLISMO], 1400.0, 10, 8)

        for monitor in [m1, m2, m3]:
            repo.crear_monitor(self.__session, monitor)

        s1 = Socio("Luis Fernandez Gil", "22334455Y", "Calle Recogidas 3", "Granada", "18004",
                   "611100200", date(1995, 4, 10), date(2023, 1, 15), date(2026, 3, 1), True, [a1, a2])
        s2 = Socio("Maria Lopez Castro", "33445566R", "Calle Arabial 7", "Granada", "18005",
                   "622200300", date(2000, 8, 20), date(2024, 6, 1), date(2025, 12, 1), True, [a3])
        s3 = Socio("Jorge Ramirez Vega", "44556677L", "Camino Ronda 12", "Granada", "18006",
                   "633300400", date(1998, 2, 14), date(2024, 3, 10), date(2026, 2, 20), True, [])

        for socio in [s1, s2, s3]:
            repo.crear_socio(self.__session, socio)

        sp1 = SocioPremium("Elena Torres Blanco", "55667788Z", "Gran Via 20", "Granada", "18007",
                           "644400500", date(1993, 6, 30), date(2022, 9, 1), date(2026, 3, 15), True, [a4, a5, a8], True)
        sp2 = SocioPremium("Roberto Navarro Diaz", "66778899D", "Calle Elvira 33", "Granada", "18008",
                           "655500600", date(1987, 12, 1), date(2023, 5, 20), date(2026, 3, 10), True, [a4, a6, a7, a8], True)

        for sp in [sp1, sp2]:
            repo.crear_socio_premium(self.__session, sp)


if __name__ == "__main__":
    gym = ZaidinGym()
    gym.main()