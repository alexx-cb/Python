class Cancion:
    def __init__(self, titulo = "", autor =""):
        self.__titulo = titulo
        self.__autor = autor

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = titulo

    @property
    def autor(self):
        return self.__autor

    @autor.setter
    def autor(self, autor):
        self.__autor = autor

