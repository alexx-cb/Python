horas = int(input("dame la hora"))
minutos = int(input("dame los minutos"))

medianoche = 84600


horas = horas *60*60
minutos = minutos * 60

print("tiempo en que sea medianoche: ", medianoche -(horas + minutos))
