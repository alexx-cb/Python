import json

data = {
  "id": 123,
  "nombre": "Ejemplo",
  "activo": True,
  "categorias": [
    {
      "id": "A1",
      "nombre": "Categoria 1",
      "items": [
        {
          "id": 1,
          "nombre": "Item 1",
          "tags": ["nuevo", "oferta"]
        },
        {
          "id": 2,
          "nombre": "Item 2",
          "tags": ["popular", "limitado"]
        }
      ]
    },
    {
      "id": "B2",
      "nombre": "Categoria 2",
      "items": [
        {
          "id": 3,
          "nombre": "Item 3",
          "tags": ["premium"]
        }
      ]
    }
  ]
}


with open("datos_formato.json", "w") as archivo:
    json.dump(data, archivo, indent=4)