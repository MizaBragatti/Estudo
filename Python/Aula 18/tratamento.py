num = 10
num2 = 0

try:
    x = num / num2
    print(x)
except ZeroDivisionError:
    print("Divisão por zero")
except:
    print("Ocorreu um erro")
else:
    print("Nenhum erro")
finally:
    print("Com/Sem erro, será executado")

try:
    f = open("arquivo.txt")
    try:
        f.write("Escrevendo no arquivo")
    except:
        print("Não foi possivel abrir o arquivo")
    finally:
        print("Fechando o arquivo")
        f.close()
except:
    print("Ocorreu algum erro na abertura do arquivo")

x = -1

# if x < 0:
#     raise Exception("O x não pode ser menor que 0")

x = "hello"

if not type(x) is int:
    raise TypeError("Somente tipos inteiros serão aceitos")


