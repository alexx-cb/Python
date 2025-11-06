# Crear un vector de 5 elementos de cadenas de caracteres, inicializa el vector con datos leídos por el
# teclado. Copia los elementos del vector en otro vector pero en orden inverso, y muéstralo por la
# pantalla.

vector1=[]

for i in range(0,5):
    vector1.append(input(f"introduce la palabra {i+1}: "))

print(vector1)

vector1.reverse()
print("Vector dado la vuelta")
print(vector1)