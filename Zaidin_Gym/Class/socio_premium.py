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
            raise ValueError("El formato de la actividad es incorrecto")

        if self.__es_premium:
            self._lista_actividades.append(actividad)
            return True
        else:
            super(SocioPremium, self).add_actividad(actividad)
            return None

    def del_actividad(self, actividad:Actividad) ->bool|None:
        super(SocioPremium, self).del_actividad(actividad)
