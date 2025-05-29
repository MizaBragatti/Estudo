diaDaSemana = 8
    
match diaDaSemana:
    case 1: 
        print("Hoje é segunda-feira")
    case 2:
        print("Hoje é terça-feira")         
    case 3:
        print("Hoje é quarta-feira")
    case 4:
        print("Hoje é quinta-feira")    
    case 5:
        print("Hoje é sexta-feira")
    case 6:
        print("Hoje é sábado")
    case 7:
        print("Hoje é domingo") 
    case _:
        print("Dia inválido, por favor insira um número entre 1 e 7")

ano = 2023
mes = 2
diaDaSemana = 2

match diaDaSemana:
    case 1 | 2 | 3 | 4 | 5 if mes == 2 and ano == 2023:
        print("Hoje é um dia de semana de fevereiro do ano 2023")
    case 6 | 7 if mes == 2 and ano == 2023:
        print("Hoje é um final de semana de fevereiro do ano 2023")
    case _:
        print("Dia inválido, por favor insira um número entre 1 e 7")
    