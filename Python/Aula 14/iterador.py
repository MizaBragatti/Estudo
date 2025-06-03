tupla = ("Maçã", "Pera", "Uva")

myit = iter(tupla)

print(next(myit))
print(next(myit))
print(next(myit))
print(type(tupla))

minhaString = "Mizael"

itString = iter(minhaString)

print(next(itString))
print(next(itString))
print(next(itString))
print(next(itString))

class minhaClasse:

    def __init__(i, nome, idade):
        i.nome = nome
        i.idade = idade

    def __iter__(i):
        i.a = 3
        return i
    
    def __next__(i):
        if i.a <= 5:
            x = i.a
            i.a += 1
            return x
        else:
            raise StopIteration



mc = minhaClasse("Mizael", 36)
print(mc.__next__)

itmc = iter(mc)

print(next(itmc))
print(next(itmc))
print(next(itmc))
print(next(itmc))

for i in itmc:
    print(i)

