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

    def __init__(self, holder:str, nif:str, pin:int, limit:int, card_number:int)->None:
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

        if not self.check_pin(pin):
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
            raise ValueError("Introduce un número positivo")

        total_gastado = self.gastado()

        if total_gastado + cantidad > self._limit:
            raise ValueError(
                f"No se puede realizar el pago: se excedería el límite de {self._limit}€ "
                f"(ya gastado: {total_gastado}€)"
            )

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

    def movimientos(self, number: int) -> list[Movimiento]:
        """
        Devuelve los últimos `number` movimientos de la tarjeta.

        :param number: int - número de movimientos que se quieren obtener
        :return: lista de objetos Movimiento (vacía si no hay movimientos)
        """
        if not TarjetaCredito._check_positive_int(number):
            raise ValueError("Introduce un número positivo")

        return self._movements[-number:][::-1]

    def numero_movimientos(self)->int:
        """
        Funcion que devuelve la longitud de la lista de movimientos
        :return: int
        """
        return len(self._movements)

    @staticmethod
    def _luhn_sum(number_str: str) -> int:
        """
        Funcion que devuelve la suma del algoritmo de Luhn
        :param number_str: str con el número de la tarjeta
        :return: int
        """
        suma = 0
        volteado = number_str[::-1]

        for index, n in enumerate(volteado):
            num = int(n)
            if index % 2 == 0:
                num *= 2
                if num > 9:
                    num -= 9
            suma += num

        return suma

    @staticmethod
    def _validar_nif(nif: str) -> bool:
        """
        Static Method que devuelve True si la letra del dni es válida
        :param nif: str con el dni completo
        :return: bool
        """
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        numero = int(nif[:8])
        letra_real = nif[8]
        return letras[numero % 23] == letra_real

    @staticmethod
    def _validar_nie(nie: str) -> bool:
        """
        Static Method que devuelve True si la letra del nie es correcta
        :param nie: str con el nie completo
        :return: bool
        """
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        conversion = {'X': '0', 'Y': '1', 'Z': '2'}

        numero = conversion[nie[0]] + nie[1:8]
        letra_real = nie[8]

        return letras[int(numero) % 23] == letra_real

    @staticmethod
    def _validar_cif(cif: str) -> bool:
        """
        Static Method que devuelve True si la letra del cif es correcta
        :param cif: str con el cif completo
        :return: bool
        """
        letras_control = "JABCDEFGHI"
        letra = cif[0]
        numeros = cif[1:8]
        control = cif[8]

        suma_par = sum(int(n) for n in numeros[1::2])
        suma_impar = 0

        for n in numeros[::2]:
            temp = int(n) * 2
            suma_impar += temp // 10 + temp % 10

        total = suma_par + suma_impar
        digito = (10 - (total % 10)) % 10

        if letra in "PQRSNW_attachment":
            return control == letras_control[digito]
        elif letra in "ABEH":
            return control == str(digito)
        else:
            return control == str(digito) or control == letras_control[digito]

    @staticmethod
    def _obtener_digito_control(number: int) -> int:
        """
        Funcion que recibe un numero de 15 digitos y devuelve el digito de control
        :param number: int con el numero de la tarjeta sin el ultimo digito
        :return: int
        """
        n_str = str(number)

        if len(n_str) != 15:
            raise ValueError("El número debe tener 15 dígitos")

        suma = TarjetaCredito._luhn_sum(n_str)
        return (10 - (suma % 10)) % 10

    @staticmethod
    def _comprobar_numero_tarjeta(number: int) -> bool:
        """
        Funcion que comprueba si el numero de la tarjeta pasa el algoritmo de Luhn
        :param number: int con el número de 16 digitos
        :return: bool
        """
        n_str = str(number)

        if len(n_str) != 16:
            return False

        digito_real = int(n_str[-1])
        numero_sin_control = int(n_str[:-1])

        digito_calculado = TarjetaCredito._obtener_digito_control(numero_sin_control)

        return digito_real == digito_calculado

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
        if not TarjetaCredito.NIF_EXPRESION.fullmatch(nif):
            return False

        if nif[0].isdigit():
            return TarjetaCredito._validar_nif(nif)
        elif nif[0] in "XYZ":
            return TarjetaCredito._validar_nie(nif)
        else:
            return TarjetaCredito._validar_cif(nif)

    @staticmethod
    def check_pin(pin: int) -> bool:
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

    @property
    def holder(self)->str:
        """
        Devuelve el nombre del titular de la tarjeta.
        """
        return self._holder

    @property
    def nif(self)->str:
        """
        Devuelve el NIF del titular de la tarjeta.
        """
        return self._nif

    @property
    def pin(self)->int:
        """
        Devuelve el PIN asociado a la tarjeta.
        """
        return self._pin

    @property
    def limit(self)->int:
        """
        Devuelve el límite de crédito de la tarjeta.
        """
        return self._limit

    @property
    def expiration_month(self)->str:
        """
        Devuelve el mes de caducidad de la tarjeta.
        """
        return self._expiration_month

    @property
    def expiration_year(self)->int:
        """
        Devuelve el año de caducidad de la tarjeta.
        """
        return self._expiration_year

    @property
    def card_number(self)->int:
        """
        Devuelve el número de la tarjeta.
        """
        return self._card_number

    @property
    def cvv(self)->int:
        """
        Devuelve el código CVV de la tarjeta.
        """
        return self._cvv

    @limit.setter
    def limit(self, limit:int)->None:
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
    def pin(self, pin:int)->None:
        """
        Establece el PIN de la tarjeta. \n

        El PIN debe tener al menos 4 dígitos.
        Lanza un ValueError si el PIN no cumple la condición.
        :param pin: int
        :return: void
        """
        if not TarjetaCredito.check_pin(pin):
            raise ValueError("El pin debe tener minimo 4 digitos")
        self._pin = pin

    def __str__(self)->str:
        """
        Funcion que devuelve una cadena de texto con los atributos del objeto
        :return: str
        """
        return (self._holder + ", " + self._nif + ", " + str(self._pin) + ", " + str(self._limit) + ", " + str(
            self._card_number)
                + ", " + str(self._expiration_year) + ", " + str(self._expiration_month) + ", " + str(
                    self._cvv) + ", " + str(self._movements))

    def __copy__(self)->TarjetaCredito:
        """
        Metodo que copia un objeto superficialmente
        :return: TarjetaCredito
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

    def __eq__(self, other:TarjetaCredito)->bool:
        """
        Metodo que compara si un objeto tiene la misma tarjeta de credito que otro
        :param other: TarjetaCredito a comparar
        :return: bool
        """
        if not isinstance(other, TarjetaCredito):
            return False
        return self._card_number == other._card_number