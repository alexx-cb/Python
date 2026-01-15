import copy
import math

from Punto import Punto

class Circulo:
    def __init__(self, centro=None, radio=0):
        if radio <0:
            raise ValueError("Radio debe ser positivo.")

        if centro is None:
            self.__centro = Punto()
        else:
            self.__centro = copy.deepcopy(centro)

        self.__radio = radio

    @classmethod
    def copia(cls, c):
        return cls(copy.deepcopy(c.__centro), c.__radio)

    @classmethod
    def circulo_origen(cls, origen_x, origen_y, radio):
        if radio < 0:
            raise ValueError("Radio debe ser positivo.")

        centro = Punto(origen_x, origen_y)
        return cls(centro, radio)


    def get_area(self):
        return math.pi * self.__radio**2

    def get_circunferencia(self):
        return 2 * math.pi * self.__radio


    @property
    def centro(self):
        return self.__centro

    @property
    def radio(self):
        return self.__radio

    @centro.setter
    def centro(self, centro):
        self.__centro = copy.deepcopy(centro)

    @radio.setter
    def radio(self, radio):
        self.__radio = copy.deepcopy(radio)


    def __str__(self):
        return "Punto:" + str(self.__centro) + "Radio:" + str(self.__radio)

    def __eq__(self, other):
        return str(self) == str(other)

class MainCirculo:
    @staticmethod
    def main():

        print("Inicializando Circulo sin parametros")
        c = Circulo()

        print(c)

        print("Inicializo un circulo con un punto y radio")

        p = Punto(3,4)
        c2 = Circulo(p, 4)

        print(c2)

        print("Copio el circulo con parametros")
        c3 = Circulo.copia(c2)

        print(c3)

        print("Cambio el radio, y el punto del circulo 3")
        c3.centro = 7,9
        c3.radio = 8
        print(c3)


        print("Creo un circulo con parametros")
        c4 = Circulo.circulo_origen(14,20,15)
        print(c4)


        print("Calculo area y diametro")
        print("area: " + str(c4.get_area()))
        print("diametro: " + str(c4.get_circunferencia()))


        copia = Circulo.copia(c4)
        print("Comprobar si un circulo es igual que otro")
        if c4 == copia:
            print("Es igual")
        else:
            print("No es igual")

        if c2 == copia:
            print("Es igual")
        else:
            print("No es igual")



if __name__ == "__main__":
    MainCirculo.main()