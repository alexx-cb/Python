hora = int(input("Ingresa la hora: "))

if 6 <= hora <= 12:
    print("Buenos días")
elif 13 <= hora <= 20:
    print("Buenas tardes")
elif hora >= 21 or hora <= 5:
    print("Buenas noches")
else:
    print("Hora no válida")