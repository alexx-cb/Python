jugador1 = input("Jugador 1, elige piedra, papel o tijera: ").strip().lower()
jugador2 = input("Jugador 2, elige piedra, papel o tijera: ").strip().lower()

opciones = ["piedra", "papel", "tijera"]

if jugador1 not in opciones or jugador2 not in opciones:
    print("Error: uno de los jugadores ha introducido una opción incorrecta.")
else:
    if jugador1 == jugador2:
        print("Empate.")
    elif (jugador1 == "piedra" and jugador2 == "tijera") or \
         (jugador1 == "papel" and jugador2 == "piedra") or \
         (jugador1 == "tijera" and jugador2 == "papel"):
        print("Gana el jugador 1.")
    else:
        print("Gana el jugador 2.")
