def funcao1():
    print('Função 1')

funcao1()

def funcaoNome(nome):
    print(f'Olá {nome}')    


funcaoNome('Mizael')

def funcNomeSobrenome(nome, sobrenome):
    print(f'Olá {nome} {sobrenome}')

funcNomeSobrenome('Mizael', 'Bragatti')

def funcaoGenerica(*args):
    for arg in args:
        print(arg)

funcaoGenerica('Mizael', 'Bragatti', 30, 'Python')

def funcaoChaveValor(arg1, arg2, arg3):
    print("The youngest child is " + arg3)


funcaoChaveValor(arg1='valor1', arg2='valor2', arg3='valor3')

def funcaoDicionario(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')


funcaoDicionario(nome='Mizael', sobrenome='Bragatti', idade=30)


def funcaoValorPadrao(nome='Mizael'):
    print(f'Olá {nome}')


funcaoValorPadrao('Eliel')
    

def funcaoLista(lista):
    print("Tipo: ", type(lista))
    for item in lista:
        print(item)


fruits = ['maçã', 'banana', 'laranja']
funcaoLista(fruits)


def funcaoSoma(a, b):
    return a + b


print("Resultado da soma:", funcaoSoma(10, 20))

def funcaoVazia():
    pass  # Função vazia, não faz nada

funcaoVazia()


def funcaoPosicional(x, /):
    print("Argumentos posicionais:", x)


funcaoPosicional("Mizael")    

def funcaoPalavraChave(*, palavra):
    print("Palavra-chave:", palavra)

funcaoPalavraChave(palavra = "Python")

def funcaoPosicionalEChave(x, /, y, *, z):
    print("Posicional:", x)
    print("Posicional:", y)
    print("Palavra-chave:", z)

funcaoPosicionalEChave(10, 20, z = 30)


def my_function(a, b, /, *, c, d, v):
  print(a + b + c + d + v)

my_function(5, 6, d = 7, c = 8, v = 9)

def fibonacci(n):
    
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
    
print("Fibonacci de 10:", fibonacci(10))