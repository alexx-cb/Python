from abc import ABC, abstractmethod


class Valorable(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def calcular_valoracion(self)->int:
        """
        Interfaz que implentan las clases ACTIVIDAD y MONITOR\n

        Devuelve un entero entre 0 y 10
        :return: int con la valoracion de la clase
        """
        pass
