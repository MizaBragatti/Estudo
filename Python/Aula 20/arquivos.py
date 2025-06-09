# import os
# #arq = open("c:\\Users\\Miza\\Documents\\Estudo\\Python\\Aula 20\\arquivo.txt")

# with open("c:\\Users\\Miza\\Documents\\Estudo\\Python\\Aula 20\\demo.txt", "w") as arq:
#     arq.write("Escrevendo uma nova linha no arquivo...\n")

# try:
#     with open("c:\\Users\\Miza\\Documents\\Estudo\\Python\\Aula 20\\demo.txt") as arq:
#         #print(arq.read())
#         #print(arq.read(10))
#         for x in arq:
#             print(x)
        
# except FileNotFoundError:
#     print("Arquivo não encontrado!")
# finally:
#     arq.close()

# # Criando novo arquivo
# try:
#     try:
#         arq = open("novoArquivo.txt", "a")
#         arq.write("Alterando novo arquivo...")
#         arq.close()
#         if os.path.exists("novoArquivo.txt"):
#             os.remove("novoArquivo.txt")
#         else:
#             print("Arquivo não existe!")
#     except FileNotFoundError:
#         print("Arquivo não encontrado!")
#     else:
#         arqNovo = open("novoArquivo.txt", "x")
# except FileExistsError:
#     print("Arquivo já existe!")

with open("arquivoOscar.txt", "w") as arquivo:
    dicionario = {"Nome": "Mizael", "Idade": 36, "Sexo": "M"}
    arquivo.write(str(dicionario))
    
with open("arquivoOscar.txt") as arq:
    print(arq.read())