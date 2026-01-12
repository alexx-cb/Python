class Cafetera:
    def __init__(self, capacidad_maxima=1000, cantidad_actual=0):

        self._capacidad_maxima = Cafetera.comprobar_entrada(capacidad_maxima)
        self._cantidad_actual = Cafetera.comprobar_entrada(cantidad_actual)

        if self._cantidad_actual > self._capacidad_maxima:
            self._cantidad_actual = self._capacidad_maxima

    @classmethod
    def cafetera_llena(cls, capacidad_maxima):
        capacidad = cls.comprobar_entrada(capacidad_maxima)
        return cls(capacidad, capacidad)

    @classmethod
    def cafetera_ajustar(cls, capacidad_maxima, cantidad_actual):
        capacidad = cls.comprobar_entrada(capacidad_maxima)
        cantidad = cls.comprobar_entrada(cantidad_actual)

        if cantidad > capacidad:
            cantidad = capacidad

        return cls(capacidad, cantidad)

    @property
    def capacidad_maxima(self):
        return self._capacidad_maxima

    @property
    def cantidad_actual(self):
        return self._cantidad_actual

    @capacidad_maxima.setter
    def capacidad_maxima(self, capacidad_maxima):
        self._capacidad_maxima = capacidad_maxima

    @cantidad_actual.setter
    def cantidad_actual(self, cantidad_actual):
        self._cantidad_actual = cantidad_actual

    def llenar_cafetera(self):
        self._cantidad_actual = self._capacidad_maxima

    def servir_taza(self, cantidad):
        if cantidad > self._cantidad_actual:
            self.cantidad_actual = 0

        else:
            self.cantidad_actual -= cantidad

    def vaciar_cafetera(self):
        self._cantidad_actual = 0

    def agregar_cafe(self, cantidad):

        self.cantidad_actual += cantidad
        if self.cantidad_actual > self._capacidad_maxima:
            self._cantidad_actual = self._capacidad_maxima


    @staticmethod
    def comprobar_entrada(dato):
        try:
            numero = int(dato)
        except ValueError:
            raise ValueError("El valor introducido no es un entero")

        if numero < 0:
            raise ValueError("El número debe ser positivo")

        return numero


def MainCafetera():
    cafetera_basica = Cafetera()

    print("Creo Una cafetera basica, capacidad de 1000 y cantidad actual 0")
    print(cafetera_basica.capacidad_maxima)
    print(cafetera_basica.cantidad_actual)

    print("Agrego 100 ml de cafe")
    cafetera_basica.agregar_cafe(100)
    print(cafetera_basica.cantidad_actual)

    print("Supero la cantidad de cafe para que llegue al limite sin pasarse")
    cafetera_basica.agregar_cafe(2000)
    print(cafetera_basica.cantidad_actual)

    print("Sirvo taza de cafe")
    cafetera_basica.servir_taza(100)
    print(cafetera_basica.cantidad_actual)

    print("Vacio la cafetera")
    cafetera_basica.vaciar_cafetera()
    print(cafetera_basica.cantidad_actual)



    print("Creo una cafetera con capacidad y cantidad variable")
    cafetera_variable = Cafetera.cafetera_ajustar(2000,500)
    print(cafetera_variable.capacidad_maxima)
    print(cafetera_variable.cantidad_actual)

    print("Creo una cafetera con la cantidad actual igual que su capacidad máxima")
    cafetera_llena = Cafetera.cafetera_llena(600)
    print(cafetera_llena.capacidad_maxima)
    print(cafetera_llena.cantidad_actual)


if __name__ == '__main__':
    MainCafetera()


