#  Igual que el programa anterior, pero esta vez la pirámide debe aparecer invertida, con el vértice
# hacia abajo.

base = 9
altura = (base +1) //2
for i in range(altura , 0, -1):
        if i == 1:
            print(" " * (altura - i) + "*")
        elif i == altura:
            print("*" * base)
        else:
            print(" " * (altura - i) + "*" + " " * (2*i - 3) + "*")