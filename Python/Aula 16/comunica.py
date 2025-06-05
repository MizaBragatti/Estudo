import json

x = '{ "name": "Miza", "age": 36, "city": "São Paulo"}'

y = json.loads(x)

print(y["name"])

x = { 
    "name": "Miza", 
    "age": 36, 
    "city": "São Paulo"
}

y = json.dumps(x)

print(y)

dict = json.dumps({"name": "John", "age": 30})
print(type(dict))
print(json.dumps(["apple", "bananas"]))
print(json.dumps(("apple", "bananas")))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))

x = {
    "nome": "Mizael",
    "idade": 36,
    "casado": True,
    "divorciado": False,
    "crianças": ("Vitória", "Lucas"),
    "animais": None,
    "carros": [
        {"modelo": "BMW 320i", "mpg": 27.5},
        {"modelo": "Ford F1000", "mpg": 24.1}
    ]
}

print(json.dumps(x, indent=1, separators=(", ", ": "), sort_keys=True))