import copy
import re
from datetime import datetime


class Movimiento:
    ALPHANUMERIC_EXPRESION = re.compile(r'^[a-zA-Z0-9]{5,50}$')

    def __init__(self, cantidad, concepto):
        """
        Constructor de la clase Movimiento. \n

        Lanza ValueError Exception si cantidad o concepto no son válidos
        :param cantidad: int con la cantidad a mover
        :param concepto: str con el concepto del movimiento
        """
        if not self._check_positive(cantidad):
            raise ValueError("La cantidad ha de ser positiva.")

        if not self._check_alphanumeric(concepto):
            raise ValueError("El concepto ha de ser alfanumerico de 5 - 50 caracteres.")

        self._cantidad = cantidad
        self._concepto = concepto
        self._fecha = datetime.now()

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def concepto(self):
        return self._concepto

    @property
    def fecha(self):
        return self._fecha

    @concepto.setter
    def concepto(self,value):
        if not Movimiento.ALPHANUMERIC_EXPRESION.fullmatch(value):
            raise ValueError("El concepto ha de ser alfanumerico de 5 - 50 caracteres")

        self._concepto = value


    @staticmethod
    def _check_positive(value :int)-> bool:
        """
        Static method para comprobar si el valor es positivo.
        :param value: int con el valor a comprobar
        :return: bool
        """
        if value <= 0:
            return True
        return False

    @staticmethod
    def _check_alphanumeric(string: str)-> bool:
        """
        Static method para comprobar si la expresion es alfanumerica de 5 - 50 caracteres.
        :param string: str con la cadena
        :return: bool
        """
        return bool(Movimiento.ALPHANUMERIC_EXPRESION.match(string))


    def __str__(self):
        return self._cantidad + ", " + self._concepto + ", " + self._fecha

    def __copy__(self):
        new_obj = type(self)(copy.copy(self._cantidad), copy.copy(self._concepto))
        new_obj._fecha = copy.copy(self._fecha)
        return new_obj

    def __eq__(self, other):
        if not isinstance(other, Movimiento):
            return False
        return self._cantidad == other._cantidad and self._concepto == other._concepto
