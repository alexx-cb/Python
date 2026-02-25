from datetime import date
import re
from abc import ABC, abstractmethod

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



        self._validar_fecha_nacimiento(fecha_nacimiento)

        self._nombre = nombre
        self._dni = dni
        self._direccion = direccion
        self._provincia = provincia
        self._codigo_postal = codigo_postal
        self._telefono = telefono
        self._fecha_nacimiento = fecha_nacimiento



    @staticmethod
    def _validar_nombre(nombre: str) -> bool:
        return bool(Persona.EXPRESION_NOMBRE.fullmatch(nombre))

    @staticmethod
    def _validar_codigo_postal(codigo_postal: str) -> bool:
        return bool(Persona.EXPRESION_CODIGO_POSTAL.fullmatch(codigo_postal))

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
