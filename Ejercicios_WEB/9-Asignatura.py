dia = input("Que dia es hoy? ")
dia = dia.lower()


if dia == "lunes":
    print("Hoy toca matematicas")
elif dia == "martes":
    print("Hoy toca lengua")
elif dia == "miercoles":
    print("Hoy toca fisica")
elif dia == "jueves":
    print("Hoy toca quimica")
elif dia == "viernes":
    print("Hoy toca frances")
else:
    print("Hoy no hay clase")