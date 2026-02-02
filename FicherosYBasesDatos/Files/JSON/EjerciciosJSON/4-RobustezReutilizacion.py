from POO.Composicion_Clases.Academia.Estudiante import Estudiante
import json

estudiantes = [
    Estudiante("Jose", "Perez", "Martinez"),
    Estudiante("Rosa", "López", "Pasadas"),
    Estudiante("Alejandro", "Valdivia", "Jimenez")
]

lista_dict = []

for e in estudiantes:
    estudiante_dict = {
        "nombre": e.nombre,
        "apellido1": e.apellido1,
        "apellido2": e.apellido2,
    }
    lista_dict.append(estudiante_dict)


with open("estudiantes.json", "w", encoding="utf-8") as archivo:
    json.dump(lista_dict, archivo, indent=4, ensure_ascii=False)


lectura_estudiantes = []

with open("estudiantes.json", "r", encoding="utf-8") as archivo:
    lista_dicts_leida = json.load(archivo)

for d in lista_dicts_leida:
    estudiante = Estudiante(
        d["nombre"],
        d["apellido1"],
        d["apellido2"],
    )
    lectura_estudiantes.append(estudiante)

for e in lectura_estudiantes:
    print(e)
