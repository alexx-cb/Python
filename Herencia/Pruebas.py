class Padre:
    def __init__(self, nombre):
        self.nombre = nombre

    def saludo(self):
        print(f"Hola soy el padre: {self.nombre}")


class Hijo(Padre):
    def __init__(self, nombre):
        super().__init__(nombre)

    def saludo(self):
        print(f"Hola soy el hijo: {self.nombre}")

