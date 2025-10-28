# Escribe un programa que muestre por pantalla 10 palabras en inglés junto a su correspondiente
# traducción al castellano. Las palabras deben estar distribuidas en dos columnas y alineadas a la
# izquierda.

ingles = ["computer", "student", "cat", "penguin", "machine", "nature", "light", "green", "book", "pyramid"]
castellano = ["ordenador", "alumno", "gato", "pingüino", "maquina", "naturaleza", "luz", "verde", "libro", "pirámide"]


for x, j in zip(ingles, castellano):
    print(f"{x:<} {j:<}")
