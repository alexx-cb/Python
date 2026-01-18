import copy

from Asignatura import Asignatura

class Estudiante:
    def __init__(self, nombre, apellido1, apellido2, lista_asignaturas = None):
        self.__nombre = nombre
        self.__apellido1 = apellido1
        self.__apellido2 = apellido2

        if lista_asignaturas is None:
            self.__lista_asignaturas = []
        else:
            self.__lista_asignaturas = lista_asignaturas


    @classmethod
    def copia(cls, e):
        return cls(nombre = e.__nombre, apellido1 = e.__apellido1, apellido2 = e.__apellido2,
                   lista_asignaturas = copy.deepcopy(e.__lista_asignaturas))


    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido1(self):
        return self.__apellido1

    @property
    def apellido2(self):
        return self.__apellido2

    @property
    def lista_asignaturas(self):
        return self.__lista_asignaturas

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @apellido1.setter
    def apellido1(self, apellido1):
        self.__apellido1 = apellido1

    @apellido2.setter
    def apellido2(self, apellido2):
        self.__apellido2 = apellido2

    @lista_asignaturas.setter
    def lista_asignaturas(self, lista_asignaturas):
        self.__lista_asignaturas = lista_asignaturas



    def agregar_asignatura(self, nueva_asignatura):
        horas_matriculadas = 0

        for asignatura in self.__lista_asignaturas:
            horas_matriculadas += asignatura.horas

        nuevas_horas = nueva_asignatura.horas

        if horas_matriculadas + nuevas_horas <=30:
            self.__lista_asignaturas.append(nueva_asignatura)
            return True
        else:
            return False


    def get_asignaturas_matriculadas(self):
        asignaturas_matriculadas = []

        for asignatura in self.__lista_asignaturas:
            asignaturas_matriculadas.append(asignatura.nombre)

        return asignaturas_matriculadas


    def get_horas_matriculadas(self):
        return sum(asignatura.horas for asignatura in self.__lista_asignaturas)


    def get_asignatura_posicion(self, posicion):

        for asignatura in range(len(self.__lista_asignaturas)):
            if asignatura == posicion:
                return self.__lista_asignaturas[asignatura]
        return None


    def __str__(self):
        return "Nombre: " + self.__nombre + ", Apellidos: " + self.__apellido1 + ", " + self.__apellido2

    def __eq__(self, other):
        if not isinstance(other, Estudiante):
            return False
        return (self.__nombre == other.__nombre and
                self.__apellido1 == other.__apellido1 and
                self.__apellido2 == other.__apellido2)

class MainEstudiante:
    @staticmethod
    def main():
        print("=== CREACIÓN DE ASIGNATURAS ===")
        a1 = Asignatura("Matemáticas", 10)
        a2 = Asignatura("Física", 8)
        a3 = Asignatura("Programación", 6)
        a4 = Asignatura("Química", 2)

        print(a1)
        print(a2)
        print(a3)
        print(a4)

        print("\n=== CREACIÓN DE ESTUDIANTE ===")
        e1 = Estudiante("Ana", "García", "López")
        print(e1)

        print("\n=== AÑADIR ASIGNATURAS ===")
        print("Añadir Matemáticas:", e1.agregar_asignatura(a1))  # True
        print("Añadir Física:", e1.agregar_asignatura(a2))  # True
        print("Añadir Programación:", e1.agregar_asignatura(a3))  # True
        print("Añadir Química (supera 30h):", e1.agregar_asignatura(a4))  # False

        print("\n=== HORAS MATRICULADAS ===")
        print("Horas totales:", e1.get_horas_matriculadas())  # 30

        print("\n=== ASIGNATURAS MATRICULADAS ===")
        print(e1.get_asignaturas_matriculadas())

        print("\n=== OBTENER ASIGNATURA POR POSICIÓN ===")
        print(e1.get_asignatura_posicion(0))  # Matemáticas
        print(e1.get_asignatura_posicion(1))  # Física
        print(e1.get_asignatura_posicion(5))  # None

        print("\n=== CONSTRUCTOR COPIA ===")
        e2 = Estudiante.copia(e1)
        print("Estudiante copia:", e2)

        print("\nAñadimos asignatura solo a la copia")
        e2.agregar_asignatura(Asignatura("Historia", 3))

        print("Horas e1:", e1.get_horas_matriculadas())  # 30
        print("Horas e2:", e2.get_horas_matriculadas())  # 33 (si se permite)

        print("\n=== COMPARACIÓN (__eq__) ===")
        e3 = Estudiante("Ana", "Martinez", "López")
        print("e1 == e3:", e1 == e3)  # True
        print("e1 == e2:", e1 == e2)  # False


if __name__ == "__main__":
    MainEstudiante.main()