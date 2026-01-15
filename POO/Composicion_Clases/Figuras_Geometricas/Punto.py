class Punto:
    def __init__(self, x=0, y=0):
        self.__x = Punto.comprobar_entero(x)
        self.__y = Punto.comprobar_entero(y)

    @classmethod
    def punto_copia(cls, p):
        return cls(x=p.__x, y=p.__y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, x):
        self.__x = Punto.comprobar_entero(x)

    @y.setter
    def y(self, y):
        self.__y = Punto.comprobar_entero(y)

    def __str__(self):
        return "(" + str(self.__x) + ", " + str(self.__y) + ")"


    def __eq__(self, other):
        return str(self) == str(other)


    @staticmethod
    def comprobar_entero(dato):
        try:
            numero = int(dato)

        except ValueError:
            raise ValueError

        return numero


class MainPunto:
    @staticmethod
    def main():

        print("Punto en (0,0)")
        p = Punto()
        print(p)

        print("Punto en (7,9)")
        p2 = Punto(7,9)
        print(p2)

        print("Cambio punto (0,0) a (14,50)")
        p.x = 14
        p.y = 50

        print(p)

        print("Nuevo punto copiado de otro")

        p3 = Punto.punto_copia(p)
        print(p3)

        print("Muestro X e Y por separado:", p.x, p.y)






if __name__ == "__main__":
    MainPunto.main()
