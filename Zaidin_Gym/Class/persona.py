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

        self._nombre = nombre
        self._dni = dni
        self._direccion = direccion
        self._provincia = provincia
        self._codigo_postal = codigo_postal
        self._telefono = telefono
        self._fecha_nacimiento = fecha_nacimiento


    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def direccion(self) -> str:
        return self._direccion

    @property
    def provincia(self) -> str:
        return self._provincia

    @property
    def codigo_postal(self) -> str:
        return self._codigo_postal

    @property
    def telefono(self) -> str:
        return self._telefono

    @property
    def fecha_nacimiento(self) -> str:
        return str(self._fecha_nacimiento)


    @nombre.setter
    def nombre(self, nombre: str):
        if not self._validar_nombre(nombre):
            raise ValueError('El nombre debe estar entre 10 y 50 caracteres')

        self._nombre = nombre

    @dni.setter
    def dni(self, dni: str):
        if not self._validar_dni(dni):
            raise ValueError("Introduce un DNI correcto")

        self._dni = dni

    @direccion.setter
    def direccion(self, direccion: str):
        self._direccion = direccion

    @provincia.setter
    def provincia(self, provincia: str):
        self._provincia = provincia

    @codigo_postal.setter
    def codigo_postal(self, codigo_postal: str):
        if not self._validar_codigo_postal(codigo_postal):
            raise ValueError("Introduce un codigo postal correcto")

        self._codigo_postal = codigo_postal

    @telefono.setter
    def telefono(self, telefono: str):
        if not self._validar_telefono(telefono):
            raise ValueError("Introduce un telefono correcto")

        self._telefono = telefono

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, fecha_nacimiento: date):
        if not self._validar_fecha_nacimiento(fecha_nacimiento):
            raise ValueError("Introduce una fecha de nacimiento correcta")

        self._fecha_nacimiento = fecha_nacimiento

    def edad(self)-> int:
        return datetime.now().year - self._fecha_nacimiento.year

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
        return (f"Persona:\n Nombre: {str(self._nombre)}\n"
                f"DNI: {str(self._dni)}\n"
                f"Direccion: {str(self._direccion)}\n"
                f"Provincia: {str(self._provincia)}\n"
                f"Codigo Postal: {str(self._codigo_postal)}\n"
                f"Telefono: {str(self._telefono)}"
                f"Fecha Nacimiento: {str(self._fecha_nacimiento)}")


    def __eq__(self, other):
        if not isinstance(other, Persona):
            return NotImplemented
        return str(self._dni) == str(other._dni)

    def __lt__(self, other):
        if not isinstance(other, Persona):
            return NotImplemented
        return self._fecha_nacimiento < other._fecha_nacimiento
