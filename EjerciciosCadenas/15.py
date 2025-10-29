# Una pastelería nos ha pedido realizar un programa que haga presupuestos de tartas. El programa
# preguntará primero de qué sabor quiere el usuario la tarta: manzana, fresa o chocolate. La tarta de
# manzana vale 18 euros y la de fresa 16. En caso de seleccionar la tarta de chocolate, el programa debe
# preguntar además si el chocolate es negro o blanco; la primera opción vale 14 euros y la segunda 15.
# Por último se pregunta si se añade nata y si se personaliza con un nombre; la nata suma 2.50 y la
# escritura del nombre 2.75.

sabor = input("Elija un sabor (manzana, fresa o chocolate): ").strip().lower()

if sabor == "manzana":
    precio_base = 18.00
elif sabor == "fresa":
    precio_base = 16.00
elif sabor == "chocolate":
    tipo_choco = input("¿Qué tipo de chocolate quiere? (negro o blanco): ").strip().lower()
    if tipo_choco == "negro":
        precio_base = 14.00
    else:
        precio_base = 15.00
else:
    print("Sabor no válido.")
    exit()


nata = input("¿Quiere nata? (si o no): ").strip().lower()
nombre = input("¿Quiere ponerle un nombre? (si o no): ").strip().lower()


precio_nata = 2.50 if nata == "si" else 0.00
precio_nombre = 2.75 if nombre == "si" else 0.00


total = precio_base + precio_nata + precio_nombre

if sabor == "chocolate":
    print(f"Tarta de chocolate {tipo_choco}: {precio_base:>6.2f} €")
else:
    print(f"Tarta de {sabor}: {precio_base:>20.2f} €")

if nata == "si":
    print(f"{'Con nata:':<20}{precio_nata:>6.2f} €")
if nombre == "si":
    print(f"{'Con nombre:':<20}{precio_nombre:>6.2f} €")

print(f"{'Total:':<20}{total:>6.2f} €")