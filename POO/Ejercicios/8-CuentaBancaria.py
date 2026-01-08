class CuentaBancaria:
    def __init__(self, saldo=0):
        if saldo < 0:
            raise ValueError

        self._saldo = saldo
        self.num_cuenta = 4564843365364

    def retirar(self, cantidad):
        if cantidad > self._saldo:
            CuentaBancaria.aplicar_agios(self)
            print("No hay suficiente saldo, se ha descontado un 5%")

        else:
            self._saldo -= cantidad

    def aplicar_agios(self):
        self._saldo -= self.saldo * 0.05

    @property
    def saldo(self):
        return self._saldo


cuenta = CuentaBancaria(45)


print(cuenta.saldo)
cuenta.retirar(50)
print(cuenta.saldo)


