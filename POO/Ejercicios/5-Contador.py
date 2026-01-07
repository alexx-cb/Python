class Contador:
    def __init__(self):
        self.contador = 0

    def incrementar(self):
        self.contador += 1

    def decrementar(self):
        self.contador += (-1)

    def obtener_valor(self):
        return self.contador

reloj = Contador()

reloj.incrementar()
reloj.incrementar()
reloj.incrementar()
reloj.incrementar()
reloj.incrementar()

print(reloj.obtener_valor())

reloj.decrementar()
reloj.decrementar()
reloj.decrementar()


print(reloj.obtener_valor())
