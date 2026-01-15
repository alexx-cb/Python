class Asignatura:
    def __init__(self, nombre, horas):
        if horas < 0:
            raise ValueError("Horas debe ser positivo.")

        self.__nombre = nombre
        self.__horas = horas

    @classmethod
    def copia(cls, a):
        return cls(nombre=a.__nombre, horas=a.__horas)

    @property
    def nombre(self):
        return self.__nombre

    @property
    def horas(self):
        return self.__horas

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @horas.setter
    def horas(self, horas):
        if horas < 0:
            raise ValueError("Horas debe ser positivo.")

        self.__horas = horas

    def __str__(self):
        return "Nombre: " + self.__nombre + " | Horas: " + str(self.__horas)

    def __eq__(self, other):
        return str(self) == str(other)


class MainAsignatura:
    @staticmethod
    def main():

        print("\n================ PRUEBA 1 =================")
        print("Crear asignatura con nombre y horas válidas")
        a1 = Asignatura("Matemáticas", 6)
        print("Asignatura creada:", a1)

        print("\n================ PRUEBA 2 =================")
        print("Acceder a los atributos usando getters")
        print("Nombre:", a1.nombre)
        print("Horas:", a1.horas)

        print("\n================ PRUEBA 3 =================")
        print("Modificar el nombre usando el setter")
        a1.nombre = "Física"
        print("Asignatura actualizada:", a1)

        print("\n================ PRUEBA 4 =================")
        print("Modificar las horas usando el setter")
        a1.horas = 8
        print("Asignatura actualizada:", a1)

        print("\n================ PRUEBA 5 =================")
        print("Crear copia de la asignatura")
        a2 = Asignatura.copia(a1)
        print("Asignatura original:", a1)
        print("Asignatura copia   :", a2)
        print("¿Son iguales?", a1 == a2)

        print("\n================ PRUEBA 6 =================")
        print("Comparar asignaturas distintas")
        a3 = Asignatura("Historia", 4)
        print("Asignatura 1:", a1)
        print("Asignatura 3:", a3)
        print("¿Son iguales?", a1 == a3)

        print("\n================ PRUEBA 7 =================")
        print("Comprobar método __str__")
        print(str(a1))

        print("\n================ PRUEBA 8 =================")
        print("Probar error al crear asignatura con horas negativas")
        try:
            a_error = Asignatura("Química", -3)
        except ValueError as e:
            print("Error capturado correctamente:", e)

        print("\n================ PRUEBA 9 =================")
        print("Probar error al modificar horas a un valor negativo")
        try:
            a1.horas = -5
        except ValueError as e:
            print("Error capturado correctamente:", e)

        print("\n======= FIN DE LAS PRUEBAS =======")





if __name__ == "__main__":
    MainAsignatura.main()



