
# criando escopo local
def minhaFuncao():
    var1 = 6
    print(var1)
    def funcaoInterna():
        print("Acesso a variavel local: ", var1)

    funcaoInterna()

minhaFuncao()

varGlobal = 10

def funcao1():
    print("Utilizando variavel global:", varGlobal)

funcao1()    

print("Chamando a variavel fora da funcao:", varGlobal)

var = 1

def escopoLocal():
    var = 2
    print(var)

escopoLocal()
print(var)

def escopoGlobal():
    global var1
    var1 = 50
    print("Interno", var1)

escopoGlobal()
print("Externo", var1)


variavelGlobal = 100

def alteraGlobal():
    global variavelGlobal
    variavelGlobal = 32
    print(variavelGlobal)

alteraGlobal()
print(variavelGlobal)

def func1():
    x = "Miza"
    def func2():
        nonlocal x
        print(x)
        x = "Paulo"

    func2()
    return x

print(func1())
    