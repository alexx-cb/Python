from Cancion import Cancion

class Album:
    def __init__(self):
        self.__canciones = []
        self.__contador = 0


    def numero_canciones(self):
        return self.__contador

    def dame_cancion(self, posicion):
        return self.__canciones[posicion]

    def agrega(self, cancion):
        self.__canciones.append(cancion)
        self.__contador += 1

    def elimina(self, posicion):
        del self.__canciones[posicion]
        self.__contador -= 1

    def graba_cancion(self, posicion, cancion):
        self.__canciones[posicion] = cancion


class MainAudioteca:

    @staticmethod
    def main():
        print("=== CREACIÓN DE CANCIONES ===")
        c1 = Cancion("Imagine", "John Lennon")
        c2 = Cancion("Bohemian Rhapsody", "Queen")
        c3 = Cancion("Hotel California", "Eagles")
        c4 = Cancion("Yesterday", "The Beatles")

        print(c1.titulo, "-", c1.autor)
        print(c2.titulo, "-", c2.autor)
        print(c3.titulo, "-", c3.autor)
        print(c4.titulo, "-", c4.autor)

        print("\n=== CREACIÓN DE ÁLBUM ===")
        album = Album()
        print("Número de canciones:", album.numero_canciones())

        print("\n=== AÑADIR CANCIONES ===")
        album.agrega(c1)
        album.agrega(c2)
        album.agrega(c3)

        print("Número de canciones:", album.numero_canciones())

        print("\n=== OBTENER CANCIONES POR POSICIÓN ===")
        print(album.dame_cancion(0).titulo)
        print(album.dame_cancion(1).titulo)
        print(album.dame_cancion(2).titulo)

        print("\n=== GRABAR (REEMPLAZAR) CANCIÓN ===")
        album.graba_cancion(1, c4)
        print(album.dame_cancion(1).titulo)

        print("\n=== ELIMINAR CANCIÓN ===")
        album.elimina(0)
        print("Número de canciones:", album.numero_canciones())
        print("Primera canción ahora:", album.dame_cancion(0).titulo)

        print("\n=== PRUEBA DE CONSISTENCIA ===")
        for i in range(album.numero_canciones()):
            cancion = album.dame_cancion(i)
            print(f"{i}: {cancion.titulo} - {cancion.autor}")

if __name__ == "__main__":
    MainAudioteca().main()

