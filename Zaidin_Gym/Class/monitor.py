from datetime import date

from Class.especialidad import Especialidad
from Class.persona import Persona
from Interface.valorable import Valorable


class Monitor(Persona, Valorable):

    def __init__(self,nombre: str, dni: str, direccion:str , provincia:str, codigo_postal:str, telefono:str,
                 fecha_nacimiento:date, especialidad:list[Especialidad], sueldo:float, votos_positivos:int, votos_negativos:int)->None:

        super().__init__(nombre, dni, direccion, provincia, codigo_postal, telefono, fecha_nacimiento)


        if not self._comprobar_especialidad(especialidad):
            raise ValueError("Un monitor no puede tener mas de 3 especialidades")

        if not self._comprobar_sueldo(sueldo):
            raise ValueError("Sueldo debe ser como minimo el salario minimo (1184€)")


        if not self._comprobar_votos(votos_positivos):
            raise ValueError("Votos positivos deben ser un numero entero positivo")

        if not self._comprobar_votos(votos_negativos):
            raise ValueError("Votos positivos deben ser un numero entero positivo")


        self.__especialidad = especialidad
        self.__sueldo = sueldo
        self.__votos_positivos = votos_positivos
        self.__votos_negativos = votos_negativos



    def me_gusta(self, like:bool)->bool:
        if like:
            self.__votos_positivos += 1
            return True
        else:
            self.__votos_negativos += 1
            return True

    def calcular_valoracion(self) ->int:
        total = self.__votos_positivos + self.__votos_negativos
        if total == 0:
            return 0

        return int((self.__votos_positivos / total) * 10)

    @property
    def especialidad(self) -> list:
        return self.__especialidad

    @property
    def sueldo(self) -> float:
        return self.__sueldo

    @especialidad.setter
    def especialidad(self,especialidad:list[Especialidad])->None:

        if not self._comprobar_especialidad(especialidad):
            raise ValueError("Un monitor no puede tener mas de 3 especialidades")

        self.__especialidad = especialidad

    @sueldo.setter
    def sueldo(self,sueldo:float)->None:
        if not self._comprobar_sueldo(sueldo):
            raise ValueError("Sueldo debe ser como minimo el salario minimo (1184€)")

        self.__sueldo = sueldo

    @staticmethod
    def _comprobar_especialidad(especialidades:list[Especialidad])->bool:
        if not isinstance(especialidades, list):
            return False

        for elemento in especialidades:
            if not isinstance(elemento, Especialidad):
                return False
        return True

    @staticmethod
    def _comprobar_sueldo(sueldo:float)->bool:
        if not isinstance(sueldo, float):
            raise TypeError('La sueldo debe ser un float')

        if sueldo <= 1184:
            return False
        return True

    @staticmethod
    def _comprobar_votos(votos)->bool:
        if not isinstance(votos, int):
            raise ValueError("Los votos deben ser un entero")

        if votos < 0:
            return False
        return True

    def __copy__(self):
        return Monitor(
            self.__nombre,
            self.__dni,
            self.__direccion,
            self.__provincia,
            self.__codigo_postal,
            self.__telefono,
            self.__fecha_nacimiento,
            self.__especialidad.copy(),
            self.__sueldo,
            self.__votos_positivos,
            self.__votos_negativos
        )


    def __str__(self):
        return super().__str__() + (f"Especialidades: {', '.join(e.value for e in self.__especialidad)}\n"
                             f"Sueldo: {self.__sueldo}\n"
                             f"Votos positivos: {self.__votos_positivos}\n"
                             f"Votos negativos: {self.__votos_negativos}\n")
