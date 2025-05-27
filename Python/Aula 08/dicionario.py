meuDicionario = {"nome": "João", "idade": 30, "cidade": "São Paulo"}
print(meuDicionario)

print(meuDicionario["nome"])

dicionarioDuplicado = {"nome": "João", "idade": 30, "cidade": "São Paulo", "nome": "Maria"}
print(dicionarioDuplicado)

tamanhoDicionario = len(meuDicionario)
print(tamanhoDicionario)    

tiposDicionario = {
    "valorString": "str",
    "valorInt": 39,
    "valorBoolean": True,
    "valorFloat": 3.14, 
    "valorLista": [1, 2, 3],
    "valorTupla": (1, 2, 3),   
    "valorSet": {1, 2, 3},
    "valorDicionario": {"chave": "valor"}
}

print(tiposDicionario)
# Acessando valores do dicionário

tipo = type(tiposDicionario)
print(tipo)

construtorDicionario = dict(nome="João", idade=30, cidade="São Paulo", sexo=["masculino", "feminino"])
print(construtorDicionario)

# Acessando valores do dicionário
print(construtorDicionario["nome"]) 

# Acessando valores do dicionário com get
print(construtorDicionario.get("idade"))

# retornando keys do dicionário
print(construtorDicionario.keys())

dictCars = { "brand": "Ford", "model": "Mustang", "year": 1964 }
# Acessando valores do dicionário

x = dictCars.keys()
print(x)

dictCars["color"] = "red"  # Adicionando um novo par chave-valor
print(x)

# retornando values do dicionário
y = dictCars.values()
print(y)

dictCars["year"] = 2020  # Atualizando o valor de uma chave existente
print(y)

dictCars["newKey"] = "newValue"  # Adicionando um novo par chave-valor
print(y)


# retornando items do dicionário
z = dictCars.items()
print(z)

# Atualizando o valor de uma chave existente
dictCars["model"] = "Fiesta"  # Atualizando o valor de uma chave existente  
print(z)

# Adicionando um novo par chave-valor
dictCars["newKey2"] = "newValue2"  # Adicionando um novo par chave-valor
print(z)

# verificando se uma chave existe no dicionário
if "brand" in dictCars:
    print("A chave 'brand' existe no dicionário.")  

#alterando o valor de uma chave existente
dictCars["brand"] = "Chevrolet"  # Alterando o valor de uma chave existente
print(dictCars)

# alterando o valor com o método update
dictCars.update({"brand": "Chevrolet", "model": "Onix"})  # Alterando o valor de uma chave existente
print(dictCars)

# incluindo uma nova chave
dictCars["newKey3"] = "newValue3"  # Incluindo uma nova chave
print(dictCars)

# adcionando uma nova chave com o método update
dictCars.update({"newKey4": "newValue4"})  # Adicionando uma nova chave
print(dictCars)

#removendo uma chave
dictCars.pop("newKey4")  # Removendo uma chave
print(dictCars)

#removendo com popitem
dictCars.popitem()  # Remove o último par chave-valor adicionado    
print(dictCars)

#removendo com del
del dictCars["newKey2"]  # Remove a chave especificada
print(dictCars)

#del dictCars
#print(dictCars)  # Isso causará um erro, pois dictCars foi deletado

# Limpando o dicionário
#dictCars.clear()  # Limpa o dicionário, removendo todos os pares chave-valor    
#print(dictCars)  # Exibe um dicionário vazio

for i in dictCars:
    print(i, " - ", dictCars[i])  # Imprime cada chave do dicionário


# utilizando o values
for i in dictCars.values():
    print(i)  # Imprime cada valor do dicionário

#utilizando o metodo keys
for i in dictCars.keys():
    print(i)  # Imprime cada chave do dicionário    

# utilizando o metodo items 
# imprime cada par chave-valor do dicionário    
for x, y in dictCars.items():
    print(x, y)  # Imprime cada par chave-valor do dicionário


# fazendo uma cópia do dicionário
dictCarsCopy = dictCars.copy()  # Faz uma cópia do dicionário
print(dictCarsCopy)  # Exibe a cópia do dicionário

#utilizando o dict
dictCarsFromDict = dict(dictCars)  # Cria um novo dicionário a partir de outro dicionário
print(dictCarsFromDict)  # Exibe o novo dicionário criado a partir de outro dicionário

#criando um dicionario aninhado
dictCarsNested = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964,
    "features": {
        "color": "red",
        "transmission": "automatic",
        "engine": {
            "type": "V8",
            "horsepower": 450
        }
    }
}
print(dictCarsNested)  # Exibe o dicionário aninhado

# criando 3 dicionários
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}    
dict3 = {"c": 5, "d": 6}
# Unindo os dicionários
dictNew = {"Dicionario1": dict1, "Dicionario2": dict2, "Dicionario3": dict3}
print(dictNew)  # Exibe o dicionário unificado

#acessando valores de dicionários aninhados
print(dictCarsNested["features"]["color"])  # Acessa o valor da chave "color" dentro de "features"
print(dictCarsNested["features"]["engine"]["type"])  # Acessa o valor da chave "type" dentro de "engine"    

# percorrendo dicionários aninhados

myfamily = {
  "child1" : {
    "name" : "Emil",
    "year" : 2004
  },
  "child2" : {
    "name" : "Tobias",
    "year" : 2007
  },
  "child3" : {
    "name" : "Linus",
    "year" : 2011
  }
}

for x, obj in myfamily.items():
    print(x)
    
    for y in obj:
        print(y + ':', obj[y])

# utilizando o método fromkeys
myDict = dict.fromkeys(["a", "b", "c"], 0)  # Cria um dicionário com chaves "a", "b" e "c" e valor inicial 0
print(myDict)  # Exibe o dicionário criado com fromkeys     

# utilizando o método setdefault
myDict.setdefault("d", 4)  # Adiciona a chave "d" com valor 4 se não existir
print(myDict)  # Exibe o dicionário após adicionar a chave "d"