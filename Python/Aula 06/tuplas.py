tupla = ('a', 'b', 'c')
# Convertendo tupla em lista
# e adicionando um elemento
lista = list(tupla)
lista.append('d')
print(lista, type(lista))

# Convertendo lista em tupla
tupla = tuple(lista)
print(tupla, type(tupla))

tupla2 = ('e',)
print(tupla2, type(tupla2))
# Concatenando tuplas
tupla += tupla2
print(tupla, type(tupla))

#removendo elementos de uma lista
lista.remove('a')
print(lista, type(lista))

tupla = tuple(lista)
print(tupla, type(tupla))

frutas = ('Maça', 'Banana', 'Laranja', 'Uva', 'Pera')

(maça, *banana, laranja) = frutas

for x in frutas:
    print(x)

for i in range(len(frutas)):
    print(frutas[i])

i = 0
print('Usando while')
# Usando while
while i < len(frutas):
    print(frutas[i])
    i = i + 1

tupla += frutas * 3
print('Unindo tuplas')
# Unindo tuplas
print(tupla, type(tupla))

#utilizando o count
print('Contando elementos')
print(tupla.count('Maça'))

#busca o índice do elemento
print('Buscando o índice do elemento')  
print(tupla.index('Banana'))