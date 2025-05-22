x = 5
y = "Texto"

print(type(x))
print(y)    

x = 10
x = "Tipo Texto"    
print(type(x))
# print(x)

# Casting
x = str(3)  # converte o número 3 para string
y = int(3.5)  # converte o número 3.5 para inteiro
z = float(3)  # converte o número 3 para float
k = bool(0)  # converte o número 0 para booleano (False)
b = bin(10)  # converte o número 10 para binário
print(x)
print(y)        
print(z)

print(type(x))
print(type(y))

print(type(z))  
print(type(k))  # imprime o tipo da variável k
print(b)  # imprime o tipo da variável b


# nome da variável não pode começar com número
# 1_nomeVariavel = "valor"
# nome da variável não pode conter caracteres especiais
# nome da variável não pode conter espaços

_nomeVariavel = "valor"
_variavel10 = "valor"
_variavel_5 = "valor minusculo"
_Variavel_5 = "Valor Maiúsculo"
printVariavel = "valor"
print(_variavel_5)
print(_Variavel_5)


camelCase = "variavel com camel case"
PascalCase = "variavel com pascal case"
snake_case = "variavel com snake case"  

var1, var2, var3 = 1, 2, 3
print(var1, var2, var3)

val1 = val2 = val3 = 5
print(val1, val2, val3)

tupla = (1, 2, 3)
v1, v2, v3 = tupla
print(v1, v2, v3)

cores = ["azul", "verde", "vermelho"]
(cor1, cor2, cor3) = cores
print(cor1, cor2, cor3)

frutas = ["banana", "maçã", "laranja", "uva", "pera"]
*fruta1, fruta2, fruta3 = frutas
print(fruta1, fruta2, fruta3)

saida1 = "Saída 1"
saida2 = "Saída 2" 
saida3 = "Saída 3"

print(saida1, saida2, saida3)
print(saida1 + saida2 + saida3)

num1 = 10
num2 = 20   
num3 = 30
print(num1 + num2 + num3)

val1 = 10
val2 = "Texto"

#print(val1 + val2)  # Isso vai gerar um erro, pois não é possível somar um número e uma string
print(val1,val2) 

variavelGlobal = "valor global"  # variável global

def funcao():
    variavelLocal = "valor local"  # variável local
    print(variavelLocal)  # imprime a variável local
    print(variavelGlobal)  # imprime a variável global  

funcao()  # chama a função
print(variavelGlobal)  # imprime a variável global  
#print(variavelLocal)  # isso vai gerar um erro, pois a variável local não pode ser acessada fora da função
# Variáveis globais e locais    

x = "awesome"

def myfunc():
    x = "fantastic"
    print("Python is " + x)

myfunc()

print("Python is " + x)  # imprime a variável global

# Variáveis globais e locais
def funcao():
    global variavelGlobal
    variavelGlobal = "valor alterado"  # altera a variável global
    print(variavelGlobal)  # imprime a variável global alterada 

funcao()  # chama a função
variavelGlobal = "valor global alterado"  # variável global
print(variavelGlobal)  # imprime a variável global alterada 