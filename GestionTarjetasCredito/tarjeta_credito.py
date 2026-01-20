import copy
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re

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
            raise ValueError("El nombre del titular debe tener entre 15 y 80 caracteres y solo puede contener letras y espacios")

        if not self._check_nif(nif):
            raise ValueError("Introduce un NIF, CIF o NIE correcto")

        if not self._check_pin(pin):
            raise ValueError("Introduce un pin correcto, minimo debe haber 4 dígitos")

        if not (500 <= limit <= 5000):
            raise ValueError("El limite debe estar entre 500 y 5000")

        if not self._check_luhn(card_number):
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

        self._cvv = random.randint(100,999)
        self._movements = []


    @staticmethod
    def _check_name(name :str) -> bool:
        """
        Static Method que devuelve si el titular entra en la expresion regular
        :param name: str con la cadena de texto
        :return: bool
        """
        return bool(TarjetaCredito.HOLDER_EXPRESION.fullmatch(name))

    @staticmethod
    def _check_nif(nif: str)-> bool:
        """
        Static Method que devuelve si el NIF, CIF o NIE esta correcto
        :param nif: str con la cadena de texto
        :return: bool
        """
        return bool(TarjetaCredito.NIF_EXPRESION.fullmatch(nif))

    @staticmethod
    def _check_pin(pin: int)-> bool:
        """
        Static Method que devuelve si el pin correcto
        :param pin: int con el pin de la tarjeta
        :return: bool
        """
        return bool(TarjetaCredito.PIN_EXPRESION.fullmatch(str(pin)))

    @staticmethod
    def _check_card(card: int)-> bool:
        """
        Static Method que devuelve si la tarjeta son 16 dígitos
        :param card: int con los digitos
        :return: bool
        """
        return bool(TarjetaCredito.CARD_EXPRESION.fullmatch(str(card)))

    @staticmethod
    def _check_luhn(number: int) -> bool:
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
                num *=2

                if num>9:
                    num -= 9
                suma += num

            else:
                suma += num

        rest = suma % 10
        if rest == 0:
            return True
        else:
            return False


    def __str__(self):
        """
        Funcion que devuelve una cadena de texto con los atributos del objeto
        :return: str
        """
        return (self._holder + ", " +self._nif +", "+ str(self._pin) +", "+ str(self._limit) +", "+ str(self._card_number)
                + ", " + str(self._expiration_year) +", "+str(self._expiration_month) + ", " + str(self._cvv) + ", "+ str(self._movements))

    def __copy__(self):
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
        if not isinstance(other, TarjetaCredito):
            return False
        return self._card_number == other._card_number

def main():
    tarjeta = TarjetaCredito("jose adfsadfasdfsdfad", "74092314E", 4785,2500,4111111111111111)
    print(tarjeta)


if __name__ == "__main__":
    main()