#  Escribe un programa que calcule el precio final de un producto según su base imponible (precio
# antes de impuestos), el tipo de IVA aplicado (general, reducido o superreducido) y el código
# promocional. Los tipos de IVA general, reducido y superreducido son del 21%, 10% y 4%
# respectivamente. Los códigos promocionales pueden ser nopro, mitad, meno5 o 5porc que significan
# respectivamente que no se aplica promoción, el precio se reduce a la mitad, se descuentan 5 euros o se
# descuenta el 5%. Mostrar los resultados tabulados

porcentaje = 0

base = int(input("Introduce la base imponible: "))
while not base.is_integer():
    print("Debes introducir un numero entero")
    base = int(input("Introduce la base imponible: "))


iva = input("Introduce el tipo de IVA (general, reducido o superreducido): ")
iva = iva.lower()

while iva not in ["general", "reducido", "superreducido"]:
    print("Debes introducir un tipo de IVA (general, reducido o superreducido): )")
    iva = input("Introduce el tipo de IVA: ")

if iva == "general":
    porcentaje = 21
elif iva == "reducido":
    porcentaje = 10
elif iva == "superreducido":
    porcentaje = 4


codigo = input("Introduce el codigo promocional (nopro, mitad, meno5 o 5porc): ")
codigo = codigo.lower()
while codigo not in ["nopro", "mitad", "meno5", "5porc"]:
    print("Debes elegir un codigo promocional (nopro, mitad, meno5 o 5porc): ")
    codigo = input("Introduce el codigo promocional: ")


precio_iva = base*porcentaje/100
precio_con_iva = precio_iva + base
precio_codigo =0

if codigo == "nopro":
    precio_codigo = -0
elif codigo == "mitad":
    precio_codigo = - precio_con_iva / 2
    precio_codigo = round(precio_codigo, 2)
elif codigo == "meno5":
    precio_codigo = -5
elif codigo == "5porc":
    precio_codigo =  -(precio_con_iva*0.05)
    precio_codigo = round(precio_codigo, 2)


print("Base imponible: ", base)
print("Precio de IVA: ", precio_iva)
print("Precio con IVA: ", precio_con_iva)
print("Cód. promo. ("+codigo+"): ", precio_codigo)
print("TOTAL: ", precio_con_iva + precio_codigo)
