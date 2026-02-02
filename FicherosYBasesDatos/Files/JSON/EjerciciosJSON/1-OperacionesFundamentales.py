import json

# 1 Exportar objeto simple a JSON
data = {"autor": "Anonimo", "version": 1.0}
with open("config.json", "w") as archivo:
    json.dump(data, archivo, indent=4)


# 2 Importar datos JSON
with open("config.json", "r") as archivo:
    data = json.load(archivo)
    print(data['version'])
