class Vehiculo:

    def __init__(self,marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def descripcion(self):
        return f"Soy un {self.modelo} de {self.marca}"

class Coche(Vehiculo):

    def __init__(self, marca, modelo, cilindros):
        super().__init__(marca, modelo)
        self.cilindros = cilindros

    def descripcion(self):
        return super().descripcion() + f" y tengo estos cilindros {self.cilindros}"

class Moto(Vehiculo):

    def __init__(self, marca, modelo, cc):
        super().__init__(marca, modelo)
        self.cc = cc

    def descripcion(self):
        return super().descripcion() + f" y tengo estos centimetros cubicos {self.cc}"


miata= Coche("Mazda", "Miata", 4)
print(miata.descripcion())

cbr = Moto("Honda", "CBR650", 650)
print(cbr.descripcion())

