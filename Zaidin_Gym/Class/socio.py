from datetime import date

from Class.actividad import Actividad
from Class.persona import Persona


class Socio(Persona):

    def __init__(self, nombre: str, dni: str, direccion:str, provincia:str, codigo_postal:str, telefono:str,
                 fecha_nacimiento:date, fecha_registro:date|None, fecha_ultimo_acceso:date, esta_activo:bool,
                 lista_actividades:None | list[Actividad]) -> None:

        super().__init__(nombre, dni, direccion, provincia, codigo_postal, telefono, fecha_nacimiento)

        if not self._validar_fecha(fecha_registro):
            raise TypeError("Formato de fecha incorrecto")

        if not self._validar_fecha(fecha_ultimo_acceso):
            raise TypeError("Formato de fecha incorrecto")

        if not self._validar_bool(esta_activo):
            raise TypeError("Formato de activo incorrecto")

        if not self._validar_lista(lista_actividades):
            raise TypeError("Formato de la lista de actividades incorrecta")

        if not self._validar_horas_actividades(lista_actividades):
            raise ValueError("La lista supera las horas necesarias")

        if fecha_registro is None:
            self.__fecha_registro = date.today()
        else:
            self.__fecha_registro = fecha_registro

        self.__fecha_ultimo_acceso = fecha_ultimo_acceso
        self.__esta_activo = esta_activo

        self.__cuota = self.get_duracion_actividades() * 6,5

        if lista_actividades is None:
            self._lista_actividades = []
        else:
            self._lista_actividades = lista_actividades


    def get_duracion_actividades(self)->int:
        return sum(actividad.duracion for actividad in self._lista_actividades)

    def add_actividad(self, actividad:Actividad) -> bool:
        if not isinstance(actividad, Actividad):
            raise TypeError("Formato de actividad incorrecto")

        if actividad.es_premium:
            raise ValueError("La actividad es para usuarios premium")

        if self.get_duracion_actividades() + actividad.duracion <6:
            self._lista_actividades.append(actividad)
            return True
        else:
            raise ValueError("No se puede agregar la actividad ya que supera el limite de horas permitido")


    def del_actividad(self, actividad:Actividad)->bool|None:
        if self._lista_actividades.remove(actividad):
            return True
        else:
            raise ValueError("No se ha podido eliminar la actividad")

    @property
    def fecha_registro(self) -> date:
        return self.__fecha_registro

    @property
    def fecha_ultimo_acceso(self) -> date:
        return self.__fecha_ultimo_acceso

    @property
    def esta_activo(self) -> bool:
        return self.__esta_activo

    @property
    def cuota(self) -> int:
        return self.__cuota

    @fecha_registro.setter
    def fecha_registro(self, fecha_registro: date) -> None:
        if not self._validar_fecha(fecha_registro):
            raise TypeError("Formato de fecha incorrecto")

        self.__fecha_registro = fecha_registro

    @fecha_ultimo_acceso.setter
    def fecha_ultimo_acceso(self, fecha_ultimo_acceso: date) -> None:
        if not self._validar_fecha(fecha_ultimo_acceso):
            raise TypeError("Formato de fecha incorrecto")

        self.__fecha_ultimo_acceso = fecha_ultimo_acceso

    @esta_activo.setter
    def esta_activo(self, esta_activo: bool) -> None:
        if not self._validar_bool(esta_activo):
            raise TypeError("Formato de activo incorrecto")

        self.__esta_activo = esta_activo

    @staticmethod
    def _validar_fecha(fecha)->bool|None:
        if not isinstance(fecha, date):
            return False
        return None

    @staticmethod
    def _validar_bool(activo)->bool|None:
        if not isinstance(activo, bool):
            return False
        return None

    @staticmethod
    def _validar_lista(lista:list) -> bool|None:
        if not isinstance(lista, list):
            return False
        return None

    #FALTA
    @staticmethod
    def _validar_horas_actividades(lista)->bool:
        return sum(actividad.duracion for actividad in lista) <= 6


    def __copy__(self):
        nuevo = Socio(
            self._nombre,
            self._dni,
            self._direccion,
            self._provincia,
            self._codigo_postal,
            self._telefono,
            self._fecha_nacimiento,
            self.__fecha_registro,
            self.__fecha_ultimo_acceso,
            self.__esta_activo,
            self._lista_actividades.copy()
        )

        nuevo.__cuota = self.__cuota

        return nuevo

    def __str__(self):
        super().__str__() + (f"\nFecha de Registro: {self.__fecha_registro}"
                             f"\nFecha ultimo acceso: {self.__fecha_ultimo_acceso}"
                             f"\nEsta Activo: {self.__esta_activo}"
                             f"\nCuota: {self.__cuota}"
                             f"\nLista de actividades: {self._lista_actividades}")

