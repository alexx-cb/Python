class CuentaSimple:
    def __init__(self, n1 = 0):
        self.saldo = n1


    def depositar_cantidad(self, valor):
        self.saldo += valor

    def retirar_cantidad(self, valor):
        self.saldo -= valor

    def obtener_saldo(self):
        return self.saldo


cuenta = CuentaSimple()

print(cuenta.obtener_saldo())
