horas = int(input("Cuantas horas has trabajado esta semana? "))

if horas >40:
    print("tu salario semanal es de: ", 40*12 + (horas-40)*16)
else:
    print("tu salario semanal es de: ", horas*12)