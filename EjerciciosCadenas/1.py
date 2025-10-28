ingles = ["computer", "student", "cat", "penguin", "machine", "nature", "light", "green", "book", "pyramid"]
castellano = ["ordenador", "alumno", "gato", "pingüino", "maquina", "naturaleza", "luz", "verde", "libro", "pirámide"]


for x, j in zip(ingles, castellano):
    print(f"{x:<} {j:<}")
