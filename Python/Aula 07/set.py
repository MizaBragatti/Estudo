meuset = {'a', 'b', 'b', 'c', 'd', 'e', 0, 1, True, False}
print(meuset)
tamanho = len(meuset)
print(tamanho)
tipo = type(meuset)
print(tipo)

construtor = set((1, 2, 3, 4, 5))
print(construtor, type(construtor))

for i in meuset:
    print(i)

print(False in meuset)
print(True not in meuset)

meuset.add('f')
print(meuset, len(meuset), type(meuset))

novoSet = {'g',}

meuset.update(novoSet)
print(meuset, len(meuset), type(meuset))

lista = [1, 2, 3, 4, 5]
meuset.update(lista)
print(meuset, len(meuset), type(meuset))

#remover um elemento
meuset.remove('g')  
print(meuset, len(meuset), type(meuset))

meuset.discard('w')  # Isso vai gerar um erro se 'w' não estiver no set
print(meuset, len(meuset), type(meuset))

itemRemovido = meuset.pop()  # Remove e retorna um item aleatório
print(itemRemovido, meuset, len(meuset), type(meuset))

meuset.clear()  # Limpa todos os elementos do set
print(meuset, len(meuset), type(meuset))

# excluir completamente o set
del meuset
#print(meuset)

#unindo todos os elementos de dois sets
set1 = {1, 2, 3}    
set2 = {'a', 'b', 'c'}
set3 = set1.union(set2)  # ou set3 = set1 | set2    
print(set3, len(set3), type(set3))
# intersecção de dois sets

#utilizando o pipe |
meuset = set1 | set2
print(meuset, len(meuset), type(meuset))

#unindo vários sets
set4 = {True, False, True}
set5 = {10, 20, 30}

meuset = set1 | set2 | set3 | set4 | set5
print(meuset, len(meuset), type(meuset))

# unindo set e lista
lista = [1, 2, 3, 4, 5] 
meuset = set1.union(lista)  # ou meuset = set1 | set(lista)
print(meuset, len(meuset), type(meuset))

#meuset = set1 | lista  # Isso não funciona, pois lista não é um set
#print(meuset, len(meuset), type(meuset))

#utilizando o update para unir sets e listas
set1.update(lista)  # Isso funciona, pois update aceita iteráveis
print(set1, len(set1), type(set1))

set1 = {1, 2, 3}
set2 = {1, 2, 4}
novoSet = set1.intersection(set2) 
print(novoSet, len(novoSet), type(novoSet))

#utilizando o & para interseção
novoSet = set1 & set2       
print(novoSet, len(novoSet), type(novoSet))

#intersection_update para interseção
set1.intersection_update(set2)  # Isso modifica set1 para conter apenas a interseção    
print(set1, len(set1), type(set1))

set3 = {True, False, True}
set4 = {1, 2, 3}
# interseção de vários sets 
novoSet = set1 & set2 & set3 & set4
print(novoSet, len(novoSet), type(novoSet), " - interseção de vários sets")

set1 = {"Apple", "Banana", "Cereja"}
set2 = {"Banana", "Damasco", "Elderberry"}

novoSet = set1.difference(set2)  # Diferença entre set1 e set2
print(novoSet, len(novoSet), type(novoSet), " - diferença entre set1 e set2")

# utilizando o - para diferença
novoSet = set1 - set2       
print(novoSet, len(novoSet), type(novoSet), " - diferença entre set1 e set2 utilizando o -")

#utilizando o difference_update para diferença
set1.difference_update(set2)  # Isso modifica set1 para conter apenas a diferença   
print(set1, len(set1), type(set1), " - diferença entre set1 e set2 utilizando o difference_update")

set1 = {"Apple", "Banana", "Cereja"}
set2 = {"Banana", "Damasco", "Elderberry"}
# Diferença simétrica entre dois sets
novoSet = set1.symmetric_difference(set2)  # Diferença simétrica entre set1 e set2  
print(novoSet, len(novoSet), type(novoSet), " - diferença simétrica entre set1 e set2")

# utilizando o ^ para diferença simétrica
novoSet = set1 ^ set2       
print(novoSet, len(novoSet), type(novoSet), " - diferença simétrica entre set1 e set2 utilizando o ^")


# utilizando o symmetric_difference_update para diferença simétrica
set1.symmetric_difference_update(set2)  # Isso modifica set1 para conter apenas a diferença simétrica       
print(set1, len(set1), type(set1), " - diferença simétrica entre set1 e set2 utilizando o symmetric_difference_update")

print(set1.isdisjoint(set2))  # Verifica se dois sets não têm elementos em comum

#verificar se um set é subconjunto de outro
print(set1.issubset(set2))  # Verifica se set1 é subconjunto de set2