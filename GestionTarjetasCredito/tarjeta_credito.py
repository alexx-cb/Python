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
        if not self._check_name(holder):
            raise ValueError("El nombre del titular debe tener entre 15 y 80 caracteres y solo puede contener letras y espacios")

        if not self._check_nif(nif):
            raise ValueError("Introduce un NIF, CIF o NIE correcto")

        if not self._check_pin(pin):
            raise ValueError("Introduce un pin correcto, minimo debe haber 4 dígitos")

        if 500 <= limit <= 5000:
            raise ValueError("El limite debe estar entre 500 y 5000")

        if not self._check_luhn(card_number):
            raise ValueError("Introduce una tarjeta de credito correcta")

        self._expiration_month = datetime.now().strftime("%m")



    @staticmethod
    def _check_name(name :str) -> bool:
        return bool(TarjetaCredito.HOLDER_EXPRESION.fullmatch(name))

    @staticmethod
    def _check_nif(nif: str)-> bool:
        return bool(TarjetaCredito.NIF_EXPRESION.fullmatch(nif))

    @staticmethod
    def _check_pin(pin: str)-> bool:
        return bool(TarjetaCredito.PIN_EXPRESION.fullmatch(pin))

    @staticmethod
    def _check_card(card: str)-> bool:
        return bool(TarjetaCredito.CARD_EXPRESION.fullmatch(card))

    @staticmethod
    def _check_luhn(number: int) -> bool:

        if not TarjetaCredito._check_card(str(number)):
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
