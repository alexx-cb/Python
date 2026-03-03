from datetime import date

from Class.persona import Persona


class Socio(Persona):

    def __init__(self, nombre: str, dni: str, direccion:str, provincia:str, codigo_postal:str, telefono:str,
                 fecha_nacimiento:date, fecha_registro:date, fecha_ultimo_acceso:date, esta_activo:bool, lista_actividades:None | list) -> None:

        super().__init__(nombre, dni, direccion, provincia, codigo_postal, telefono, fecha_nacimiento)

        if not self._validar_fecha(fecha_registro):
            raise TypeError("Formato de fecha incorrecto")

        if not self._validar_fecha(fecha_ultimo_acceso):
            raise TypeError("Formato de fecha incorrecto")

        if not self._validar_activo(esta_activo):
            raise TypeError("Formato de activo incorrecto")

        self.__fecha_registro = fecha_registro
        self.__fecha_ultimo_acceso = fecha_ultimo_acceso
        self.__esta_activo = esta_activo

        # FALTA IMPLEMETAR
        self.__cuota = 0

        if lista_actividades is None:
            self._lista_actividades = []
        else:
            self._lista_actividades = lista_actividades


    #FALTA IMPLEMENTAR
    # def get_duracion_activiades(self):

    # def add_actividad(self, Actividad):

    # def del_actividad(self, Actividad):

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
        if not self._validar_activo(esta_activo):
            raise TypeError("Formato de activo incorrecto")

        self.__esta_activo = esta_activo

    @staticmethod
    def _validar_fecha(fecha):
        if not isinstance(fecha, date):
            raise TypeError("Formato de fecha incorrecto")

    @staticmethod
    def _validar_activo(activo):
        if not isinstance(activo, bool):
            raise TypeError("Formato de activo incorrecto")

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

