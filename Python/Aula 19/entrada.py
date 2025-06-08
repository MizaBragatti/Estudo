import math
# print("Informe seu nome:")
# nome = input()
# print(f"Seu nome é: {nome}")

# nome = input("Informe seu nome...")
# idade = input("Informe sua idade...")
# estado = input("Informe seu estado civil...")
# print(f"Seu nome é: {nome}, idade: {idade} e estado civil: {estado}")

#x = input("Informe um valor:")
# y = math.sqrt(float(x))
# print( f"A raiz quadrada de {x} é igual a {y}")


y = True
while y == True:
    x = input("Informe um valor:")
    try:
        x = float(x)
        y = False
    except:
        print("Entrada errada, insira outro valor.")

print("Obrigado!")