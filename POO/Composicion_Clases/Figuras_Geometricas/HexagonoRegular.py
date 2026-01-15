import copy
import doctest
import math

from Punto import Punto


class HexagonoRegular:
    def __init__(self,centro = None,lado=1):
        if lado <0:
            raise ValueError("Lado debe ser positivo y mayor que 0.")

        if centro is None:
            self.__centro = Punto()
        else:
            self.__centro = copy.deepcopy(centro)

        self.__lado = lado

    @classmethod
    def copia(cls, h):
        return cls(copy.deepcopy(h.__centro),h.__lado )

    @classmethod
    def hexagono_origen(cls, origen_x, origen_y, lado):
        if lado <0:
            raise ValueError("Lado debe ser positivo y mayor que 0.")

        centro = Punto(origen_x,origen_y)

        return cls(centro,lado)

    def get_diametro(self):
        return self.__lado*6


    def get_area(self):

        apotema = math.sqrt(self.__lado**2 - (self.__lado/2)**2)

        return ((self.__lado * 6) * apotema)/2


    @property
    def centro(self):
        return self.__centro

    @property
    def lado(self):
        return self.__lado

    @centro.setter
    def centro(self,centro):
        self.__centro = copy.deepcopy(centro)

    @lado.setter
    def lado(self,lado):
        self.__lado = copy.deepcopy(lado)

    def __str__(self):
        return "Punto: " + str(self.__centro) + "Lado: " + str(self.__lado)

    def __eq__(self,other):
        return  str(self) == str(other)


class MainHexagonoRegular:
    @staticmethod
    def main():
        print("\n================ PRUEBA 1 =================")
        print("Crear hexágono por defecto")
        h1 = HexagonoRegular()
        print("Hexágono creado:", h1)

        print("\n================ PRUEBA 2 =================")
        print("Crear hexágono con centro (2,3) y lado 4")
        p = Punto(2, 3)
        h2 = HexagonoRegular(p, 4)
        print("Hexágono creado:", h2)

        print("\n================ PRUEBA 3 =================")
        print("Crear hexágono usando el método de clase hexagono_origen")
        h3 = HexagonoRegular.hexagono_origen(5, 5, 6)
        print("Hexágono creado:", h3)

        print("\n================ PRUEBA 4 =================")
        print("Crear copia de un hexágono")
        h4 = HexagonoRegular.copia(h2)
        print("Hexágono original:", h2)
        print("Hexágono copia   :", h4)
        print("¿Son iguales?", h2 == h4)

        print("\n================ PRUEBA 5 =================")
        print("Comprobar getters")
        print("Centro de h2:", h2.centro)
        print("Lado de h2:", h2.lado)

        print("\n================ PRUEBA 6 =================")
        print("Calcular diámetro")
        print("Lado:", h2.lado)
        print("Diámetro:", h2.get_diametro())

        print("\n================ PRUEBA 7 =================")
        print("Calcular área")
        print("Lado:", h2.lado)
        print("Área:", h2.get_area())

        print("\n================ PRUEBA 8 =================")
        print("Modificar centro usando setter")
        nuevo_centro = Punto(10, 10)
        h2.centro = nuevo_centro
        print("Nuevo centro:", h2.centro)

        print("\n================ PRUEBA 9 =================")
        print("Modificar lado usando setter")
        h2.lado = 8
        print("Nuevo lado:", h2.lado)
        print("Hexágono actualizado:", h2)

        print("\n================ PRUEBA 10 =================")
        print("Comparar dos hexágonos distintos")
        print("h1:", h1)
        print("h2:", h2)
        print("¿Son iguales?", h1 == h2)

        print("\n================ PRUEBA 11 =================")
        print("Probar error al usar lado negativo")
        try:
            h_error = HexagonoRegular(Punto(0, 0), -5)
        except ValueError as e:
            print("Error capturado correctamente:", e)

        print("\n================ PRUEBA 12 =================")
        print("Probar error en hexagono_origen con lado negativo")
        try:
            h_error2 = HexagonoRegular.hexagono_origen(0, 0, -3)
        except ValueError as e:
            print("Error capturado correctamente:", e)

        print("\n======= FIN DE LAS PRUEBAS =======")






if __name__ == "__main__":
    MainHexagonoRegular.main()

