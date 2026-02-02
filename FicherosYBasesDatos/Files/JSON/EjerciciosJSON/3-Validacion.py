import json

# 4 Exportar una lista de diccionarios
data = {
    "productos": [
        {"nombre":"Laptop", "precio":1200}
    ]
}

with open("productos.json", "w") as archivo:
    json.dump(data, archivo, indent=4)


new_product={"nombre":"Iphone", "precio":700}


try:
    data["productos"].append(new_product)
    with open("productos.json", "w") as archivo:
        json.dump(data, archivo, indent=4)

except json.JSONDecodeError as e:
    print(f"Error al agregar el producto: {e}")


# 5 Filtrado Basico de Datos
with open("productos.json", "r") as archivo:
    data = json.load(archivo)

producto = [iterator for iterator in data["productos"] if iterator["precio"]>1000]
print(producto)