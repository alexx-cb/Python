class Empleado:
    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos

    def nombre_completo(self):
        return self.nombre + " " + self.apellidos

empleado = Empleado("Alberto", "Gonzalez")
print(empleado.nombre_completo())