#criando uma classe

class minhaClasse:
    print("minha classe")


mc = minhaClasse()

print(type(mc))


class Pessoa:
    def __init__(obj, nome, idade):
        obj.nome = nome
        obj.idade = idade

    def __str__(obj):
        return f"{obj.nome}({obj.idade})"
    
    def getNome(obj):
        return obj.nome

    def getIdade(obj):
        return obj.idade


p1 = Pessoa("Mizael", 36)
p1.idade = 37

print(p1, type(p1))
# print(p1.nome, type(p1))
# print(p1.idade)

print(p1.getNome())
#del p1.idade;
print(p1.getIdade())

#del p1

print(p1)

class Carro:

    def __init__(c, marca, modelo, ano):
        c.marca = marca
        c.modelo = modelo
        c.ano = ano

    def getMarca(c):
        return c.marca
    def getModelo(c):
        return c.modelo
    def getAno(c):
        return c.ano
    

class Estudante(Pessoa):
    def __init__(obj, nome, idade, ano):
        super().__init__(nome, idade)
        obj.graduacao = ano

    def bemVindo(obj):
        print("Bem vindo", obj.nome, obj.idade, "a turma de :", obj.graduacao)


#estudante1 = Estudante("Oscar", "43")

# print(estudante1)

# estudante1.idade = 44

# print(estudante1.idade)

x = Estudante("Adilson", 38, 2020)

x.bemVindo()

    


