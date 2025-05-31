carros = ["Fusca", "Civic", "Corolla", "Onix", "Gol"]

print("Carros:", carros)
print("Primeiro carro:", carros[0])
print("Segundo carro:", carros[1])

#alterando o valor do primeiro carro
carros[0] = "Kombi"

print("Primeiro carro:", carros[0])

print("Tamanho da lista:", len(carros))


#Imprimindo todos os carros
for carro in carros:
    print("Carro:", carro)


# Adicionando um carro
carros.append("Palio")

for carro in carros:
    print("Carro:", carro)


# Removendo todos os carros 1 a 1

tamanho = len(carros)

i = 0
#utilizando o loop for
for i in range(tamanho):
    carro = carros[0]  # Sempre remove o primeiro carro
    carros.pop(0)
    print("Removendo carro:", carro)
print("Carros restantes:", carros)
# Verificando se a lista está vazia

fruits = ["Maçã", "Banana", "Laranja", "Uva", "Banana", "Pera", "Melancia"]
print("Frutas:", fruits)

fruits.remove("Banana")
print("Frutas após remoção:", fruits)

fruits.clear()  # Limpa a lista
print("Frutas após limpeza:", fruits)

fruits.insert(0, "Kiwi")  # Adiciona Kiwi na posição 0
fruits.insert(1, "Abacaxi")  # Adiciona Abacaxi na posição 1
fruits.append("Manga")  # Adiciona Manga no final da lista  
fruits.append("Morango")  # Adiciona Morango no final da lista
print("Frutas após inserção:", fruits)

fruits.sort()  # Ordena a lista
print("Frutas após ordenação:", fruits)

fruits.reverse()  # Inverte a lista
print("Frutas após inversão:", fruits)