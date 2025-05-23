var = "Oscar"


#print(var[0])


#for x in var:  
 #   print(x)
    
#print(len(var))  # imprime do índice 0 ao 2 (não inclui o 2)

variavel = "Esse texto contem o nome Mizael e o sobrenome Silva"

#print("Mizael" in variavel)  # True

if "Oscar" not in variavel:
    print("Oscar não está na variável")

print(variavel[10:15])  # imprime do índice 0 ao 4 (não inclui o 5)
print(variavel[10:])  # imprime do índice 0 ao 4 (não inclui o 5)
print(variavel[:5])  # imprime do índice 0 ao 4 (não inclui o 5)    
print(variavel[-1])  # imprime o último caractere
print(variavel[-2])  # imprime o penúltimo caractere

varNum = 2
#$2varNum

#print(var + varNum)  # imprime tudo em maiúsculo

price = 59.12
txt = f"The price is {price:.2f} dollars"
print(txt)

l1 = "Mizael   forcar uma aspa \\ \"  Adilson\t\t\t outro texto \x48\x65\x6c\x6c\x6f"
print(l1)

var2 = ("texto1", "texto2", "texto3")
print("-".join(var2))