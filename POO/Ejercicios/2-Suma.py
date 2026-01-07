class Suma:
    def __init__(self, n1= 154, n2 =34):
        self.n1= n1
        self.n2= n2

    def obtener_suma(self) -> int:
        return self.n1 + self.n2

print(Suma().obtener_suma())