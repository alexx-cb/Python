from datetime import date, datetime
import re
from abc import ABC

class Persona(ABC):

    EXPRESION_NOMBRE= re.compile(r'^(?=.{10,50}$)[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$')
    EXPRESION_DNI = re.compile(r'^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]+$')
    EXPRESION_CODIGO_POSTAL = re.compile(r'^[0-9]{5}$')
    EXPRESION_TELEFONO = re.compile(r'^[0-9]{9}$')

    def __init__(self, nombre: str, dni: str, direccion:str , provincia:str, codigo_postal:str,
                 telefono:str, fecha_nacimiento:date)->None:

        if not self._validar_nombre(nombre):
            raise ValueError('El nombre debe estar entre 10 y 50 caracteres')

        if not self._validar_dni(dni):
            raise ValueError("Introduce un DNI correcto")

        if not self._validar_codigo_postal(codigo_postal):
            raise ValueError("Introduce un codigo postal correcto")

        if not self._validar_telefono(telefono):
            raise ValueError("Introduce un telefono correcto")

        self._validar_fecha_nacimiento(fecha_nacimiento)

        self.__nombre = nombre
        self.__dni = dni
        self.__direccion = direccion
        self.__provincia = provincia
        self.__codigo_postal = codigo_postal
        self.__telefono = telefono
        self.__fecha_nacimiento = fecha_nacimiento


    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def dni(self) -> str:
        return self.__dni

    @property
    def direccion(self) -> str:
        return self.__direccion

    @property
    def provincia(self) -> str:
        return self.__provincia

    @property
    def codigo_postal(self) -> str:
        return self.__codigo_postal

    @property
    def telefono(self) -> str:
        return self.__telefono

    @property
    def fecha_nacimiento(self) -> date:
        return self.__fecha_nacimiento


    @nombre.setter
    def nombre(self, nombre: str):
        if not self._validar_nombre(nombre):
            raise ValueError('El nombre debe estar entre 10 y 50 caracteres')

        self.__nombre = nombre

    @dni.setter
    def dni(self, dni: str):
        if not self._validar_dni(dni):
            raise ValueError("Introduce un DNI correcto")

        self.__dni = dni

    @direccion.setter
    def direccion(self, direccion: str):
        self.__direccion = direccion

    @provincia.setter
    def provincia(self, provincia: str):
        self.__provincia = provincia

    @codigo_postal.setter
    def codigo_postal(self, codigo_postal: str):
        if not self._validar_codigo_postal(codigo_postal):
            raise ValueError("Introduce un codigo postal correcto")

        self.__codigo_postal = codigo_postal

    @telefono.setter
    def telefono(self, telefono: str):
        if not self._validar_telefono(telefono):
            raise ValueError("Introduce un telefono correcto")

        self.__telefono = telefono

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, fecha_nacimiento: date):
        if not self._validar_fecha_nacimiento(fecha_nacimiento):
            raise ValueError("Introduce una fecha de nacimiento correcta")

        self.__fecha_nacimiento = fecha_nacimiento

    def edad(self)-> int:
        return datetime.now().year - self.__fecha_nacimiento.year

    @staticmethod
    def _validar_nombre(nombre: str) -> bool:
        return bool(Persona.EXPRESION_NOMBRE.fullmatch(nombre))

    @staticmethod
    def _validar_codigo_postal(codigo_postal: str) -> bool:
        return bool(Persona.EXPRESION_CODIGO_POSTAL.fullmatch(codigo_postal))

    @staticmethod
    def _validar_telefono(telefono: str) -> bool:
        return bool(Persona.EXPRESION_TELEFONO.fullmatch(telefono))

    @staticmethod
    def _validar_dni(dni : str)->bool:

        if not Persona.EXPRESION_DNI.fullmatch(dni):
            return False

        return Persona._validar_letra_dni(dni)

    @staticmethod
    def _validar_letra_dni(dni : str)->bool:
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        numero = int(dni[:8])
        letra_real = dni[8]
        return letras[numero % 23] == letra_real

    @staticmethod
    def _validar_fecha_nacimiento(fecha:date)->None:

        if not isinstance(fecha, date):
            raise TypeError('Formato de fecha no valido')

        hoy = date.today()
        edad = hoy.year - fecha.year

        if (hoy.month , hoy.day) < (fecha.month, fecha.day):
            edad -= 1

        if edad < 0:
            raise ValueError('La fecha no puede ser futura')

        if edad > 99:
            raise ValueError('No puedes tener mas de 99 años')

    def __str__(self):
        return (f"\nPersona:\nNombre: {str(self.__nombre)}\n"
                f"DNI: {str(self.__dni)}\n"
                f"Direccion: {str(self.__direccion)}\n"
                f"Provincia: {str(self.__provincia)}\n"
                f"Codigo Postal: {str(self.__codigo_postal)}\n"
                f"Telefono: {str(self.__telefono)}\n"
                f"Fecha Nacimiento: {str(self.__fecha_nacimiento)}")


    def __eq__(self, other):
        if not isinstance(other, Persona):
            return NotImplemented
        return str(self.__dni) == str(other.__dni)

    def __lt__(self, other):
        if not isinstance(other, Persona):
            return NotImplemented
        return self.__fecha_nacimiento < other.__fecha_nacimiento
