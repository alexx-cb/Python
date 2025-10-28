comida = input("¿Qué has tomado para comer? (tostada, churros o donut): ").lower()

precio_comida = 0

if comida == "churros":
    precio_comida = 1.50
elif comida == "donut":
    precio_comida = 1.00
elif comida == "tostada":
    tipo_tostada = input("¿Tostada básica o especial?: ").lower()
    if tipo_tostada == "básica" or tipo_tostada == "basica":
        precio_comida = 1.20
    elif tipo_tostada == "especial":
        precio_comida = 1.60
    else:
        print("Tipo de tostada no válido.")
        exit()
else:
    print("Opción de comida no válida.")
    exit()

bebida = input("¿Qué has tomado para beber? (zumo o café): ").lower()

if bebida == "zumo":
    precio_bebida = 1.80
elif bebida == "café" or bebida == "cafe":
    precio_bebida = 1.20
else:
    print("Opción de bebida no válida.")
    exit()

total = precio_comida + precio_bebida

print(f"El precio total del desayuno es: {total:.2f}€")
