# La tienda online BanderaDeEspaña.es vende banderas personalizadas de la máxima calidad y nos
# ha pedido hacer un configurador que calcule el precio según el alto y el ancho. El precio base de una
# bandera es de un céntimo de euro el centímetro cuadrado. Si la queremos con un escudo bordado, el
# precio se incrementa en 2.50 € independientemente del tamaño. Los gastos de envío son 3.25 €. El IVA
# ya está incluido en todas las tarifas.

altura = int(input("Introduce la altura de la bandera en cm: "))
ancho = int(input("Introduce el ancho ahora: "))
escudo = input("¿Quiere escudo bordado? (s/n): ")


precio_bandera = altura * ancho / 100
precio_total = precio_bandera
precio_escudo = 2.5
envio = 3.25

if escudo == "s":
    precio_total += precio_escudo


precio_total += envio

print("Aqui tiene el desglose de su compra")

print(f"{f'Bandera de {altura*ancho} cm2':<20} {precio_bandera:>10.2f} €")
print(f"{"Sin escudo":<20} {0:>10}" if escudo == "n" else f"{"Con escudo":<20} {precio_escudo:>10} €")
print(f"{"Gastos de envio":<20} {envio:>10} €")
print(f"{"Total":<20} {precio_total:>10} €")
