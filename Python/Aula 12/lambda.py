multiplicacao = lambda a, b: a * b
print(multiplicacao(5, 3))

soma = lambda a, b, c: a + b + c
print(soma(1, 2, 3))

def myfunc(x):
    return lambda y: x * y

myDoubler = myfunc(2)
myTripler = myfunc(3)
print(myDoubler(11))  # Output: 22
print(myTripler(11))  # Output: 22


pessoas = [
    {"nome": "Ana", "idade": 25},
    {"nome": "Bruno", "idade": 20},
    {"nome": "Carlos", "idade": 30}
]

# Ordena a lista pelo campo 'idade'
pessoas_ordenadas = sorted(pessoas, key=lambda pessoa: pessoa["idade"])

print(pessoas_ordenadas)