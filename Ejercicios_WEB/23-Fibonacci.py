n = int(input("¿Cuántos términos de la serie de Fibonacci quieres mostrar?: "))

a, b = 0, 1
contador = 0

print("Serie de Fibonacci:")

while contador < n:
    print(a)
    a, b = b, a + b
    contador += 1