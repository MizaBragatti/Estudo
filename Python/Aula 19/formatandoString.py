txt = f"Meu texto formatado"

print(txt)

preco = 59

txt = f"O preco da bola é de {preco:.2f}"
print(txt)

txt = f"O preco da bola é de {35:.2f}"
print(txt)

txt = f"A soma de 25 + 35 = {25+35:.2f}"
print(txt)

valor1 = 25
valor2 = 45
txt = f"A multiplicação de {valor1} * {valor2} = {valor1*valor2:.2f}"
print(txt)

valor = 35

txt = f"O valor está muito {'Caro' if valor > 35 else 'Barato'}"
print(txt)

def meuMetodo():
    return 35

txt = f"Imprimindo valor do método: {meuMetodo()}"
print(txt)

valorCasa = 100000
txt = f"O valor da casa ficou em: {valorCasa:,}"
txt = f"O valor da casa ficou em: {valorCasa :<5} espaços"
txt = f"O valor da casa ficou em: {valorCasa:_}"
txt = f"O valor da casa ficou em: {valorCasa:b}"
txt = f"O valor da casa ficou em: {valorCasa:o}"
txt = f"O valor da casa ficou em: {valorCasa:X}"
print(txt)


