# Se quiere realizar un programa que lea por teclado las 5 notas obtenidas por un alumno
# (comprendidas entre 0 y 10). A continuación debe mostrar todas las notas, la nota media, la nota más
# alta que ha sacado y la menor

notas = []

for i in range(0, 10):
    nota = float(input(f"Digite su nota {i+1}: "))

    while nota < 0 or nota > 10:
        print("Valor invalido, la nota debe estar entre 0 y 10")
        nota = float(input(f"Digite su nota {i+1}: "))

    notas.append(nota)



media = 0
print("\nTodas las notas")


for index,nota in enumerate(notas):
    media += nota
    print(f"nota {index+1}: ", nota)

notas.sort()

print("\nnota mas baja: ", notas[0])
print("\nnota mas alta: ", notas[9])

media = media/len(notas)
print("\nmedia de notas: ", media)

