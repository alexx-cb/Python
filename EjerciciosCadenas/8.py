# Escribe un programa que pinte por pantalla una pirámide rellena a base de asteriscos. La base de la
# pirámide debe estar formada por 9 asteriscos.

base = 9

altura = (base + 1) // 2
for i in range(1, altura +1):
    estrellas = "*" * (2 * i - 1)
    espacios = " " * (altura - i)
    print(espacios + estrellas)