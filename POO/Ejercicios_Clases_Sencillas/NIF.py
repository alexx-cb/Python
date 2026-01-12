class NIF:
    def __init__(self, numero=0, letra=" "):
        self._numero= numero
        self._letra = letra


    @classmethod
    def establecer_letra(cls, numero):
        cls._numero = numero

        letra = cls.calcular_letra(numero)

        return cls(numero, letra)


    def leer(self):
        while True:
            try:
                numero = int(input("Introduce el número: "))
                if numero <= 0 or len(str(numero)) != 8:
                    raise ValueError

                self._numero = numero
                self._letra = self.calcular_letra(numero)
                break

            except ValueError:
                print("Introduce un número positivo de 8 dígitos")




    @staticmethod
    def calcular_letra(numero):
        posibles_letras = ["T", "R", "W", "A", "G", "M", "Y", "F", "P", "D", "X", "B", "N", "J", "Z", "S", "Q", "V",
                           "H", "L", "C", "K", "E"]
        return posibles_letras[numero % 23]


    def __str__(self):
        return str(self._numero)+ "-" + self._letra


    @property
    def numero(self):
        return self._numero

    @property
    def letra(self):
        return self._letra

    @numero.setter
    def numero(self, numero):
        self._numero = numero

    @letra.setter
    def letra(self, letra):
        self._letra = letra


def main():

    print("Creo un objeto vacio")
    vacio = NIF()

    print("Leo por teclado un numero y se lo asigno al objeto vacio")
    vacio.leer()
    print(vacio)



    print("Creo un objeto con un numero por parametro y se le asigna una letra")
    dni = NIF.establecer_letra(14589657)
    print(dni)


    print("Numero: ", dni.numero)
    print("Letra: ", dni.letra)

    dni.numero= 45976849
    dni.letra = "A"

    print("Numero cambiado: ", dni.numero)
    print("Letra cambiada: ", dni.letra)




if __name__ == "__main__":
    main()