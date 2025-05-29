# condicional

var1 = 50
var2 = 30

if var1 < var2:
    print("var1 é menor que var2")
elif var1 == var2:
    print("var1 é  igual que var2")
else:
    print("var1 é maior a var2")

#utilizando o if na mesma linha
print("var1 é menor que var2") if var1 < var2 else print("var1 é maior ou igual a var2")

a = 10
b = 20


print("A") if a > b else print("=") if a == b else print("B")

# Utilizando o and  
if var1 < 100 and var2 < 100:
    print("var1 e var2 são menores que 100")

# Utilizando o or
if var1 < 100 or var2 > 100:
    print("var1 ou var2 são menores que 100")

#utilizando o not
if not var1 > 100:
    print("var1 não é maior que 100")


if var1 < 100:
    if var2 < 100:
        print("var1 e var2 são menores que 100")
        if var1 < 50:
            pass




#crie um lista
# lista = [d['a'], d['b'], d['c'], d['d']]
# crie uma tupla
# tupla = (d['a'], d['b'], d['c'], d['d'])
# #crie um conjunto
# conjunto = {d['a'], d['b'], d['c'], d['d']}
# #crie um dicionário
# dicionario = {'a': d['a'], 'b': d['b'], 'c': d['c'], 'd': d['d']}   

d = {'a': 0, 'b': 1, 'c': 0, 'd': 1}

if d['a'] > 0:
    print('ok')
elif d['b'] > 1:
    print('ok - cair aqui')
elif d['c'] > 0:
    print('ok')
elif d['d'] > 0:
    print('ok')
else:
    print('not ok')    

x = 10
y = 20
if x < y: print('foo'); print('bar'); print('baz')