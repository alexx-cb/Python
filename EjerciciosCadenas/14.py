# Realiza un programa que calcule el precio de unas entradas de cine en función del número de
# personas y del día de la semana. El precio base de una entrada son 8 euros. El miércoles (día del
# espectador), el precio base es de 5 euros. Los jueves son el día de la pareja, por lo que la entrada para
# dos cuesta 11 euros. Con la tarjeta CineCampa se obtiene un 10% de descuento. Si un jueves, un
# grupo de 6 personas compran entradas, el precio total sería de 33 euros ya que son 3 parejas; pero si es
# un grupo de 7, pagarán 3 entradas de pareja más 1 individual que son 41 euros (33 + 8).


print("Venta de entradas CineCampa")

num_entradas = int(input("Número de entradas: "))
dia_semana = input("Día de la semana: ").strip().lower()
tarjeta = input("¿Tiene tarjeta CineCampa? (s/n): ").strip().lower()


precio_base = 8.0
precio_pareja = 11.0

if dia_semana == "miércoles" or dia_semana == "miercoles":
    precio_base = 5.0
    total = num_entradas * precio_base
    tipo = "individual"
    parejas = 0

elif dia_semana == "jueves":
    parejas = num_entradas // 2
    sueltas = num_entradas % 2
    total = parejas * precio_pareja + sueltas * precio_base
    tipo = "pareja"

else:
    total = num_entradas * precio_base
    tipo = "individual"
    parejas = 0
    sueltas = 0

if tarjeta == "s":
    descuento = total * 0.10
else:
    descuento = 0.0

a_pagar = total - descuento

print("\nAquí tiene sus entradas. Gracias por su compra.")

if dia_semana == "jueves":
    print(f"{'Entradas de parejas':<30}{parejas:>5}")
    print(f"{'Precio por entrada de pareja':<30}{precio_pareja:>6.2f} €")
else:
    print(f"{'Entradas individuales':<30}{num_entradas:>5}")
    print(f"{'Precio por entrada individual':<30}{precio_base:>6.2f} €")

print(f"{'Total':<30}{total:>6.2f} €")
print(f"{'Descuento':<30}{descuento:>6.2f} €")
print(f"{'A pagar':<30}{a_pagar:>6.2f} €")