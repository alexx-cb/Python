# Igual que el programa anterior, pero esta vez la pirámide estará hueca (se debe ver únicamente el
# contorno hecho con asteriscos).

base = 9
altura = (base +1) //2
for i in range(1, altura + 1):
        if i == 1:
            print(" " * (altura - i) + "*")
        elif i == altura:
            print("*" * base)
        else:
            print(" " * (altura - i) + "*" + " " * (2*i - 3) + "*")