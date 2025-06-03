str = "Mizael Bragatti"

# contar letras de uma string
print(len(str))

tupla = ("a", "b", "c")

# contar itens da tupla
print(len(tupla))

dicionario = {"ch1": "1", "ch2": "2", "ch3": "3", "ch4": "4"}

# contar chave/valor de um dicionario
print(len(dicionario))

class Veiculo:
    def __init__(obj, marca, modelo):
        obj.marca = marca
        obj.modelo = modelo

    def move(obj):
        print("Dirigir", obj.marca, obj.modelo)

class Carro(Veiculo):
    pass

class Barco(Veiculo):
    def move(obj):
        print(2)      

class Aviao(Veiculo):
    def move(obj):
        print(3)       

carro = Carro("Honda", "Fit")           
barco = Barco("Barc", "B1" )
aviao = Aviao("Caça", "C1")

for i in (carro, barco, aviao):
    i.move()