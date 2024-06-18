
import json

# Dataset de amigos em Salvador, Bahia
friends = {
    "Joao": {"latitude": -12.9714, "longitude": -38.5014},
    "Pedro": {"latitude": -12.9822, "longitude": -38.4653},
    "Maria": {"latitude": -12.9486, "longitude": -38.3535},
    "Ana": {"latitude": -12.9250, "longitude": -38.4192},
    "Carlos": {"latitude": -12.9348, "longitude": -38.5012},
    "Fernanda": {"latitude": -12.9718, "longitude": -38.4542},
    "Bruno": {"latitude": -12.9734, "longitude": -38.5042},
    "Renata": {"latitude": -12.9777, "longitude": -38.4894},
    "Luciana": {"latitude": -12.9657, "longitude": -38.5068},
    "Gustavo": {"latitude": -12.9760, "longitude": -38.4916}
}

# Locais em Salvador, Bahia
places_salvador = {
    "Farol da Barra": {"latitude": -13.0103, "longitude": -38.5253},
    "Pelourinho": {"latitude": -12.9714, "longitude": -38.5096},
    "Elevador Lacerda": {"latitude": -12.9716, "longitude": -38.5108},
    "Mercado Modelo": {"latitude": -12.9714, "longitude": -38.5133},
    "Igreja do Bonfim": {"latitude": -12.9239, "longitude": -38.5045}
}

data = {"friends": friends, "places_salvador": places_salvador}

# Salvar o dicionário como um arquivo JSON
with open('database.json', 'w') as f:
    json.dump(data, f, indent=4)
