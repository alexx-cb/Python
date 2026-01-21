import copy
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
from movimiento import Movimiento


class TarjetaCredito:
    HOLDER_EXPRESION = re.compile(r'^(?=.{15,80}$)[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$')
    NIF_EXPRESION = re.compile(
        r'^(?:[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]|'
        r'[XYZ][0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKE]|'
        r'[ABCDEFGHJKLMNPQRSUVW][0-9]{7}[0-9A-J])$'
    )
    PIN_EXPRESION = re.compile(r'^[0-9]{4,}$')
    CARD_EXPRESION = re.compile(r'^[0-9]{16}$')

    def __init__(self, holder, nif, pin, limit, card_number):
        """
        Constructor por defecto de la clase TarjetaCredito \n

        Lanza ValueError Exception si alguno de los datos introducidos es incorrecto

        :param holder: titular de la tarjeta, 15 - 80 caracteres
        :param nif: DNI, CIF o NIE del titular
        :param pin: PIN para la tarjeta, mínimo 4 dígitos
        :param limit: Límite de gasto para la tarjeta, debe estar entre 500 y 5000
        :param card_number: Número de la tarjeta de credito, deben ser 16 dígitos y pasar el algoritmo de Luhn
        """
        if not self._check_name(holder):
            raise ValueError(
                "El nombre del titular debe tener entre 15 y 80 caracteres y solo puede contener letras y espacios")

        if not self._check_nif(nif):
            raise ValueError("Introduce un NIF, CIF o NIE correcto")

        if not self._check_pin(pin):
            raise ValueError("Introduce un pin correcto, minimo debe haber 4 dígitos")

        if not (500 <= limit <= 5000):
            raise ValueError("El limite debe estar entre 500 y 5000")

        if not self._comprobar_numero_tarjeta(card_number):
            raise ValueError("Introduce una tarjeta de credito correcta")

        self._holder = holder
        self._nif = nif
        self._pin = int(pin)
        self._limit = limit
        self._card_number = int(card_number)
        self._expiration_month = datetime.now().strftime("%m")

        current_year = datetime.now()
        expiration_date = current_year + relativedelta(years=5)
        self._expiration_year = expiration_date.year

        self._cvv = random.randint(100, 999)
        self._movements = []

    def pagar(self, cantidad: float, concepto: str) -> bool:
        """
        Funcion que permite hacer un pago con la tarjeta. \n

        Agrega al atributo de movements un nuevo movimiento con la cantidad y el concepto
        :param cantidad: float con la cantidad del pago
        :param concepto: str con el concepto del pago
        :return: bool
        """
        if not Movimiento.check_positive(cantidad):
            raise ValueError("Introduce un numero positivo")

        if cantidad > self._limit:
            raise ValueError("La cantidad del pago no debe ser superior al limite de pago")

        if not Movimiento.check_alphanumeric(concepto):
            raise ValueError("El concepto debe ser una cadena alfanumérica de 5 - 50 caracteres")

        mov = Movimiento(cantidad, concepto)
        self._movements.append(mov)

        return True

    def gastado(self)->float:
        """
        Funcion que devuelve el gasto total de la tarjeta
        :return: float
        """
        suma =0
        for move in self._movements:
            suma += move.cantidad

        return suma


    def movimientos(self, number:int):
        """
        Funcion que devuelve los ultimo n movimientos
        :param number: int numero de los ultimos movimientos
        :return: obj
        """
        if not TarjetaCredito._check_positive_int(number):
            raise ValueError("Introduce un numero positivo")

        for move in self._movements[-number:]:
            return move
        return None

    def numero_movimientos(self):
        """
        Funcion que devuelve la longitud de la lista de movimientos
        :return: int
        """
        return len(self._movements)




    @staticmethod
    def _check_positive_int(number:int)->bool:
        """
        Static Method que devuelve si el numero positivo y entero
        :param number:
        :return:
        """
        return isinstance(number, int) and not isinstance(number, bool) and number > 0

    @staticmethod
    def _check_name(name: str) -> bool:
        """
        Static Method que devuelve si el titular entra en la expresion regular
        :param name: str con la cadena de texto
        :return: bool
        """
        return bool(TarjetaCredito.HOLDER_EXPRESION.fullmatch(name))

    @staticmethod
    def _check_nif(nif: str) -> bool:
        """
        Static Method que devuelve si el NIF, CIF o NIE esta correcto
        :param nif: str con la cadena de texto
        :return: bool
        """
        return bool(TarjetaCredito.NIF_EXPRESION.fullmatch(nif))

    @staticmethod
    def _check_pin(pin: int) -> bool:
        """
        Static Method que devuelve si el pin correcto
        :param pin: int con el pin de la tarjeta
        :return: bool
        """
        return bool(TarjetaCredito.PIN_EXPRESION.fullmatch(str(pin)))

    @staticmethod
    def _check_card(card: int) -> bool:
        """
        Static Method que devuelve si la tarjeta son 16 dígitos
        :param card: int con los digitos
        :return: bool
        """
        return bool(TarjetaCredito.CARD_EXPRESION.fullmatch(str(card)))

    @staticmethod
    def _comprobar_numero_tarjeta(number: int) -> bool:
        """
        Static Method que devuelve si el número de la tarjeta de crédito pasa el algoritmo de Luhn
        :param number: int con el número de la tarjeta
        :return: bool
        """

        if not TarjetaCredito._check_card(number):
            return False

        n_str = str(number)

        volteado = n_str[::-1]
        suma = 0

        for index, n in enumerate(volteado):
            num = int(n)
            if index % 2 != 0:
                num *= 2

                if num > 9:
                    num -= 9
                suma += num

            else:
                suma += num

        rest = suma % 10
        if rest == 0:
            return True
        else:
            return False

    @property
    def holder(self):
        """
        Devuelve el nombre del titular de la tarjeta.
        """
        return self._holder

    @property
    def nif(self):
        """
        Devuelve el NIF del titular de la tarjeta.
        """
        return self._nif

    @property
    def pin(self):
        """
        Devuelve el PIN asociado a la tarjeta.
        """
        return self._pin

    @property
    def limit(self):
        """
        Devuelve el límite de crédito de la tarjeta.
        """
        return self._limit

    @property
    def expiration_month(self):
        """
        Devuelve el mes de caducidad de la tarjeta.
        """
        return self._expiration_month

    @property
    def expiration_year(self):
        """
        Devuelve el año de caducidad de la tarjeta.
        """
        return self._expiration_year

    @property
    def card_number(self):
        """
        Devuelve el número de la tarjeta.
        """
        return self._card_number

    @property
    def cvv(self):
        """
        Devuelve el código CVV de la tarjeta.
        """
        return self._cvv

    @limit.setter
    def limit(self, limit):
        """
        Establece el límite de crédito de la tarjeta. \n

        El límite debe estar comprendido entre 500 y 5000.
        Lanza un ValueError si el valor no es válido.
        :param limit: int
        :return: void
        """
        if not (500 <= limit <= 5000):
            raise ValueError("El limite debe estar entre 500 y 5000")
        self._limit = limit

    @pin.setter
    def pin(self, pin):
        """
        Establece el PIN de la tarjeta. \n

        El PIN debe tener al menos 4 dígitos.
        Lanza un ValueError si el PIN no cumple la condición.
        :param pin: int
        :return: void
        """
        if not TarjetaCredito._check_pin(pin):
            raise ValueError("El pin debe tener minimo 4 digitos")
        self._nif = pin

    def __str__(self):
        """
        Funcion que devuelve una cadena de texto con los atributos del objeto
        :return: str
        """
        return (self._holder + ", " + self._nif + ", " + str(self._pin) + ", " + str(self._limit) + ", " + str(
            self._card_number)
                + ", " + str(self._expiration_year) + ", " + str(self._expiration_month) + ", " + str(
                    self._cvv) + ", " + str(self._movements))

    def __copy__(self):
        """
        Metodo que copia un objeto superficialmente
        :return: obj
        """
        new_obj = type(self)(
            self._holder,
            self._nif,
            self._pin,
            self._limit,
            self._card_number
        )
        new_obj._expiration_month = self._expiration_month
        new_obj._expiration_year = self._expiration_year
        new_obj._cvv = self._cvv
        new_obj._movements = copy.copy(self._movements)
        return new_obj

    def __eq__(self, other):
        """
        Metodo que compara si un objeto tiene la misma tarjeta de credito que otro
        :param other: obj a comparar
        :return: bool
        """
        if not isinstance(other, TarjetaCredito):
            return False
        return self._card_number == other._card_number


def main():
    tarjeta = TarjetaCredito("jose adfsadfasdfsdfad", "74092314E", 4785, 2500, 4111111111111111)
    print(tarjeta)


if __name__ == "__main__":
    main()