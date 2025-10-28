CLAVE_SECRETA = "4825"

intentos = 4

for intento in range(1, intentos + 1):
    entrada = input(f"Intento {intento}/{intentos} - Introduce un número de 4 cifras: ").strip()

    if not (len(entrada) == 4 and entrada.isdigit()):
        print("Formato incorrecto: debes introducir exactamente 4 cifras.")
    elif entrada == CLAVE_SECRETA:
        print("La caja fuerte se ha abierto.")
        break
    else:
        print("Lo siento, esa no es la combinación.")

else:
    print("Se han agotado los intentos. La caja fuerte sigue cerrada.")
