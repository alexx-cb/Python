import copy
import re
from datetime import datetime


class Movimiento:
    ALPHANUMERIC_EXPRESION = re.compile(r'^[a-zA-Z0-9 ]{5,50}$')

    def __init__(self, cantidad: float, concepto:str, fecha=None)->None:
        """
        Constructor de la clase Movimiento. \n

        Lanza ValueError Exception si cantidad o concepto no son válidos
        :param cantidad: int con la cantidad a mover
        :param concepto: str con el concepto del movimiento
        """
        if not self.check_positive(cantidad):
            raise ValueError("La cantidad ha de ser positiva.")

        if not self.check_alphanumeric(concepto):
            raise ValueError("El concepto ha de ser alfanumerico de 5 - 50 caracteres.")

        self._cantidad = cantidad
        self._concepto = concepto

        if fecha is None:
            self._fecha = datetime.now()
        elif isinstance(fecha, str):
            self._fecha = datetime.fromisoformat(fecha)
        elif isinstance(fecha, datetime):
            self._fecha = fecha
        else:
            raise TypeError("Fecha debe ser datetime o str en formato ISO")

    @classmethod
    def from_dict(cls, data):
        """
        Crea un Movimiento desde un diccionario, convirtiendo la fecha a datetime si es string.
        """
        return cls(
            cantidad=data["cantidad"],
            concepto=data["concepto"],
            fecha=data.get("fecha")
        )

    def to_dict(self)->dict:

        movimiento = {
            "cantidad" : self._cantidad,
            "concepto" : self._concepto,
            "fecha" : self._fecha.isoformat() if isinstance(self._fecha, datetime) else self._fecha,
        }
        return movimiento

    @property
    def cantidad(self)->float:
        """
        Getter de cantidad
        :return: int
        """
        return self._cantidad

    @property
    def concepto(self)->str:
        """
        Getter de concepto
        :return: str
        """
        return self._concepto

    @property
    def fecha(self)->datetime:
        """
        Getter de fecha
        :return: datetime
        """
        return self._fecha

    @concepto.setter
    def concepto(self,concepto:str)->None:
        """
        Setter de concepto \n

        Lanza ValueError si no pasa la expresion regular
        :param concepto: str con el concepto del movimiento
        :return: void
        """
        if not Movimiento.ALPHANUMERIC_EXPRESION.fullmatch(concepto):
            raise ValueError("El concepto ha de ser alfanumerico de 5 - 50 caracteres")

        self._concepto = concepto

    @staticmethod
    def check_positive(value :float)-> bool:
        """
        Static method para comprobar si el valor es positivo.
        :param value: float con el valor a comprobar
        :return: bool
        """
        if value <= 0:
            return False
        return True

    @staticmethod
    def check_alphanumeric(string: str)-> bool:
        """
        Static method para comprobar si la expresion es alfanumerica de 5 - 50 caracteres.
        :param string: str con la cadena
        :return: bool
        """
        return bool(Movimiento.ALPHANUMERIC_EXPRESION.match(string))

    def __str__(self)->str:
        """
        Metodo que devuelve un str con los atributos del objeto
        :return: str
        """
        return "Cantidad: " + str(self._cantidad) + ", Concepto: " + self._concepto + ", Fecha: " + str(self._fecha)

    def __copy__(self)->Movimiento:
        """
        Metodo que copia un objeto superficialmente
        :return: obj
        """
        new_obj = type(self)(copy.copy(self._cantidad), copy.copy(self._concepto))
        new_obj._fecha = copy.copy(self._fecha)
        return new_obj

    def __eq__(self, other:Movimiento)->bool:
        """
        Metodo que compara si un objeto es igual a otro
        :param other: obj
        :return: bool
        """
        if not isinstance(other, Movimiento):
            return False
        return self._cantidad == other._cantidad and self._concepto == other._concepto and self._fecha == other._fecha