nota1 = float(input("Introduce la nota del primer examen: "))
nota2 = float(input("Introduce la nota del segundo examen: "))


media = (nota1 + nota2) / 2

if media >= 5:
    print(f"Has aprobado con una media de {media:.2f}")
else:
    resultado = input("¿Cuál ha sido el resultado de la recuperación? (apto/no apto): ").strip().lower()
    if resultado == "apto":
        media = 5
    print(f"Tu nota final es {media:.2f}")
