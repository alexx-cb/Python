class Alumno:
    def __init__(self, nombre, apellidos, edad):
        self.nombre = nombre
        self.apellidos = apellidos
        self.edad = edad

    def nombre_apellido(self):
        return self.nombre + " " + self.apellidos

    @property
    def edad(self):
        return self.edad
    
    @edad.setter
    def edad(self, value):
        if value<1:
            raise ValueError("El edad debe ser mayor que 0")
        self._edad = value


    def __str__(self):
        return self.nombre + " " + self.apellidos + " " + str(self.edad)

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        if isinstance(other, Alumno):
            return str(self.edad) < str(other.edad)
        raise TypeError




al1 = Alumno("Jose", "Martinez", 30)
al2 = Alumno("Jose", "Martinez", 19)
al3 = Alumno("Jose", "Martinez", 10)

alumnos = [al1, al2, al3]

for a in alumnos:
    print(a)

alumnos.sort()

for a in alumnos:
    print(a)

if al1 == al2:
    print("Es el mismo alumno")
else:
    print("Es diferente alumno")



print(al1)