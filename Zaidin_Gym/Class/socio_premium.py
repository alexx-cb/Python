from datetime import date

from Class.actividad import Actividad
from Class.socio import Socio


class SocioPremium(Socio):
    def __init__(self, nombre: str, dni: str, direccion:str, provincia:str, codigo_postal:str, telefono:str,
                 fecha_nacimiento:date, fecha_registro:date, fecha_ultimo_acceso:date, esta_activo:bool,
                 lista_actividades:None | list[Actividad], es_premium:bool):
        super().__init__(nombre, dni, direccion, provincia, codigo_postal, telefono, fecha_nacimiento, fecha_registro,
                         fecha_ultimo_acceso, esta_activo, lista_actividades)


        if not self._validar_bool(es_premium):
            raise ValueError("Introduce un valor valido para premium")

        self.__es_premium = es_premium



    def add_actividad(self, actividad:Actividad) -> bool|None:
        if not isinstance(actividad, Actividad):
            raise ValueError("Formato incorrecto")

        self._lista_actividades.append(actividad)
        return True

    def del_actividad(self, actividad:Actividad) ->bool|None:
        return super().del_actividad(actividad)

    @staticmethod
    def _permite_actividades_premium() -> bool:
        return True

    def _validar_horas_actividades(self, lista) -> bool:
        return True

    def __str__(self):
        return super().__str__() + f"\nPremium: {self.__es_premium}\n"