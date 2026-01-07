class Estudiante:
    def __init__(self, nombre, nota1,nota2):
        self.nombre = nombre
        self.nota1 = nota1
        self.nota2 = nota2

    def calcular_media(self) -> float:
        return (self.nota1 + self.nota2) / 2

    def mostrar_datos(self) -> str:
        return "Nombre: " +str(self.nombre) + ". Nota media: " + str(self.calcular_media())

alumno = Estudiante("Jose", 8.66,4.9)

print(alumno.mostrar_datos())