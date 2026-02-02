import json

data = {
    "programadores":[
        {"nombre": "Pepe", "lenguaje":"C++", "nivel":7},
        {"nombre": "Jose", "lenguaje":"Python", "nivel":5}
    ]
}

json_str = json.dumps(data, indent=4)
print(json_str)

with open ("programadores.json", "w") as archivo:
    json.dump(data, archivo, indent=4)
