class RectanguloBasico:
    def __init__(self, largo, ancho):
        self.largo = largo
        self.ancho = ancho

    def calcular_area(self) -> float:
        return self.largo * self.ancho


rectangulo = RectanguloBasico(5, 7)
print("area del rectangulo: ", rectangulo.calcular_area())