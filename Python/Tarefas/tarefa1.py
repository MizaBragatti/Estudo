# # Programa feito em Python que gerencia uma lista de alunos e suas notas.
 

# Criando variáveis para armazenar os dados dos alunos
alunos = {"nomes": [], "idade": [],"notas": []}

# Função para adicionar um aluno e sua nota
def adicionar_aluno(nome, idade, nota):
    if nome in alunos["nomes"]:
        pass
        #print(f"Aluno {nome} já está cadastrado.")
    else:
        alunos["nomes"].append(nome)
        alunos["idade"].append(idade)
        alunos["notas"].append(nota)
        #print(f"Aluno {nome} adicionado com nota {nota}.")


adicionar_aluno("João", 20, 8.5)
adicionar_aluno("Maria", 22, 9.0)   
adicionar_aluno("João", 20, 8.5)  # Tentativa de adicionar aluno já existente
adicionar_aluno("Ana", 19, 7.5) 

# Criar um Set com as matérias e permitir adicionar e remover matérias
materias = set()
def adicionar_materia(materia):
    if materia in materias:
        return
    materias.add(materia)

def remover_materia(materia):
    if materia in materias:
        materias.remove(materia)

adicionar_materia("Matemática")
adicionar_materia("Português")
adicionar_materia("História")
adicionar_materia("Matemática")  # Tentativa de adicionar matéria já existente
remover_materia("História")  # Tentativa de remover matéria não cadastrada
remover_materia("Matemática")
adicionar_materia("Geografia")
adicionar_materia("Biologia")
adicionar_materia("Química")
    


#Função para calcular a média das notas, utilizando Casting para float
def calcular_media():
    # utilizando o conceito de Casting para converter as notas para float
    media = sum(float(nota) for nota in alunos["notas"]) / len(alunos["notas"])
    print(f"Média das notas: {media:.2f}")


# Verificar se aluno foi aprovado ou reprovado informando o nome do aluno por parâmetro
def verificar_aprovacao(nome):
    aprovado = False
    if nome in alunos["nomes"]:
        index = alunos["nomes"].index(nome)
        nota = alunos["notas"][index]
        if nota >= 7.0:
            aprovado = True
    print(f"{nome} foi aprovado?", aprovado)
    
    
# 1 - Alunos cadastrados
# Criar uma função que retorne uma lista com os nomes dos alunos cadastrados
def exibir_alunos():
    lista_alunos = []
    for nome in alunos["nomes"]:
        lista_alunos.append(nome)   
    print("Alunos cadastrados:", lista_alunos)


# 2 - Notas dos alunos
# Criar uma função que retorne um dicionário com os nomes e as notas dos alunos
def exibir_notas():
    notas_alunos = {}
    for i in range(len(alunos["nomes"])):
        notas_alunos[alunos["nomes"][i]] = alunos["notas"][i]
    print("Notas:", notas_alunos)

# 3 - Matérias disponíveis
# Criar uma função que retorne um conjunto com as matérias disponíveis, somente com o nome da matéria 

def exibir_materias():
    if materias:
        print("Matérias disponíveis:", materias)
    else:
        print("Nenhuma matéria cadastrada.")


# 4 - Média das notas
# 5 - Verificar se aluno foi aprovado ou reprovado

def resumo_alunos():
    print("\nResumo dos Alunos:")
    exibir_alunos()
    exibir_notas()
    exibir_materias()
    calcular_media()
    verificar_aprovacao("João")

resumo_alunos()


# Desafio Extra:
# Permitir que o usuário adicione novos alunos e notas através do teclado.

def adicionar_aluno_teclado():
    nome = input("Digite o nome do aluno: ")
    idade = int(input("Digite a idade do aluno: "))
    nota = float(input("Digite a nota do aluno: "))
    adicionar_aluno(nome, idade, nota)
    print(f"Aluno {nome} adicionado com nota {nota}.")

adicionar_aluno_teclado()    
resumo_alunos()