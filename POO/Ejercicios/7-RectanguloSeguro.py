class Rectangulo:
    def __init__(self, largo, ancho):
        self._largo = largo
        self._ancho = ancho

    def obtener_area(self):
        return self._largo * self._ancho

    @property
    def largo(self):
        return self._largo

    @property
    def ancho(self):
        return self._ancho

    @largo.setter
    def largo(self, valor):
        if valor <= 0:
            raise ValueError('Largo debe ser mayor que 0')
        self._largo = valor



rec = Rectangulo(5, 5)
print(rec.obtener_area())

rec.largo = 10
print(rec.obtener_area())

print(rec.largo)
print(rec.ancho)