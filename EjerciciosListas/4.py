# Queremos guardar los nombres y la edades de los alumnos de un curso. Realiza un programa que
# introduzca el nombre y la edad de cada alumno. El proceso de lectura de datos terminará cuando se
# introduzca como nombre un asterisco (*) Al finalizar se mostrará los siguientes datos:
# • Todos los alumnos mayores de edad.
# • Los alumnos mayores (los que tienen más edad)

alumnos = []

while True:
    nombre = input("Introduce el nombre (* para salir): ")
    if nombre == "*":
        break

    while True:
        try:
            edad = int(input("Introduce su edad: "))
            if edad < 0:
                print("La edad no puede ser negativa. Intenta de nuevo.")
            else:
                break
        except ValueError:
            print("Por favor, introduce un número válido para la edad.")

    alumnos.append([nombre, edad])


print("Alumnos mayores de edad")

for alumno in alumnos:
    if alumno[1] >= 18:
        print(alumno[0])

# Ordeno alumnos por edad
alumnos.sort(key=lambda x: x[1], reverse=True)

print("alumno de mayor edad")

for alumno in alumnos[:1]:
    print(alumno[0], alumno[1])

