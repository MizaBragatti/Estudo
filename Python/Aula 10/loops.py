

i = 1

while i <= 10:
    print("valor = ", i)
    i = i + 1
else:
    print("Loop terminado, i =", i)
    
i = 1
while True:
    print("valor =", i)
    if i >= 10:
        break  # Sai do loop quando i chega a 10
    i += 1

fruits = ["maçã", "banana", "laranja"]

for i in fruits:
    print("fruta =", i)


# exemplo com Dictionary
variavelDict = {
    "nome": "João", 
    "idade": 30, 
    "cidade": "São Paulo"
}
for chave, valor in variavelDict.items():
    print("chave =", chave, ", valor =", valor)


variavelString = "Python"
for i in variavelString:
    print("letra =", i)


listaNomes = ["Ana", "Bruno", "Carlos", "Miza", "Adilson", "Oscar"]

for i in listaNomes:
    
    if i == "Miza":
        print("Miza encontrado, saindo do loop")
        continue  # Sai do loop quando encontra "Miza"
    print("nome =", i)

for x in range(5, 16, 2):
    print("x =", x)
    if x == 11:
        print("11 encontrado, saindo do loop")
        break
else:
    print("Loop com range terminado, x =", x)   


# Exemplo de loop aninhado
for i in range(1, 4):
    for j in range(1, 4):
        print(f"i = {i}, j = {j}")

# Exemplo prático do uso de pass: cadastro de usuários, mas ainda não implementado

usuarios = ["Ana", "Bruno", "Carlos", "Miza"]

for usuario in usuarios:
    if usuario == "Miza":
        # Ainda não implementamos o cadastro para o usuário "Miza"
        pass
    else:
        print(f"Cadastrando usuário: {usuario}")

print("Processo de cadastro finalizado.")        