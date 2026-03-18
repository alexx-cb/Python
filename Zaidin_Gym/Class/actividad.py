from Class.especialidad import Especialidad
from Interface.valorable import Valorable


class Actividad(Valorable):
    def __init__(self, nombre:str, duracion: int, calorias:int, categoria: Especialidad, es_premium:bool) -> None:
        super().__init__()

        if not self._comprobar_duracion(duracion):
            raise ValueError("La duracion de la clase debe ser mayor a 1 minuto y menor que 2 horas")


        if not self._comprobar_positivo(calorias):
            raise ValueError("No se pueden poner calorias negativas")

        if not self._comprobar_categoria(categoria):
            raise ValueError("La categoria no esta validada")


        if not self._comprobar_premium(es_premium):
            raise ValueError("Introduce un valor correcto para el parametro es_premium")


        self.__nombre = nombre
        self.__duracion = duracion
        self.__calorias = calorias
        self.__categoria = categoria
        self.__es_premium = es_premium
        self.__votos= []


    def votar(self, voto:int)->bool|None:
        if 0<=voto<=10:
            self.__votos.append(voto)
            return True
        return None

    def calcular_valoracion(self) -> int:
        if not self.__votos:
            return 0
        return sum(self.__votos) // len(self.__votos)


    @property
    def nombre(self)->str:
        return self.__nombre

    @property
    def duracion(self)->int:
        return self.__duracion

    @property
    def calorias(self)->int:
        return self.__calorias

    @property
    def categoria(self)->Especialidad:
        return self.__categoria

    @property
    def es_premium(self)->bool:
        return self.__es_premium

    @nombre.setter
    def nombre(self, nombre:str)->None:
        self.__nombre = nombre

    @duracion.setter
    def duracion(self, duracion:int)->None:
        if not self._comprobar_duracion(duracion):
            raise ValueError("La duracion de la clase debe ser mayor a 1 minuto y menor que 2 horas")

        self.__duracion = duracion

    @calorias.setter
    def calorias(self, calorias:int)->None:
        if not self._comprobar_positivo(calorias):
            raise ValueError("No se pueden poner calorias negativas")

        self.__calorias = calorias

    @categoria.setter
    def categoria(self, categoria:Especialidad)->None:
        if not self._comprobar_categoria(categoria):
            raise ValueError("La categoria no esta validada")
        self.__categoria = categoria

    @es_premium.setter
    def es_premium(self, es_premium:bool)->None:
        if not self._comprobar_premium(es_premium):
            raise ValueError("Introduce un valor correcto para el parametro es_premium")

        self.__es_premium = es_premium

    @staticmethod
    def _comprobar_premium(premium:bool)->bool:
        if not isinstance(premium, bool):
            return False
        else:
            return True

    @staticmethod
    def _comprobar_categoria(categoria:Especialidad)->bool:
        if not isinstance(categoria, Especialidad):
            return False
        else:
            return True

    @staticmethod
    def _comprobar_positivo(n:int)->bool:
        if n<=0:
            return False
        else:
            return True

    @staticmethod
    def _comprobar_duracion(duracion:int)->bool:
        if duracion <= 0 or duracion > 120:
            return False
        else:
            return True

    def __eq__(self, other) -> bool:
        if not isinstance(other, Actividad):
            raise ValueError("No se puede comparar el tipo de Actividad")

        return (
                self.__nombre == other.__nombre and
                self.__duracion == other.__duracion and
                self.__categoria == other.__categoria
        )

    def __lt__(self, other) -> bool:
        if not isinstance(other, Actividad):
            raise ValueError("No se puede comparar el tipo de Actividad")

        if self.__nombre == other.__nombre:
            return self.__duracion < other.__duracion

        return self.__nombre < other.__nombre

    def __str__(self)->str:
        return str(f"Nombre: {self.__nombre}\n"
                   f"Duracion: {self.__duracion}\n"
                   f"Calorias: {self.__calorias}\n"
                   f"Categoria: {self.__categoria.name}\n"
                   f"Premium: {self.__es_premium}\n"
                   f"Valoracion: {self.calcular_valoracion()}\n")
