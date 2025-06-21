import requests

def listarRegistro(registro):
    requisicao = requests.get('https://jsonplaceholder.typicode.com/posts/' + str(registro))
    if requisicao.status_code == 200:
        return requisicao.json()
    else:
        return f"Erro: {requisicao.status_code}"

def listarTudo():
    requisicao = requests.get('https://jsonplaceholder.typicode.com/posts')
    if requisicao.status_code == 200:
        return requisicao.json()
    else:
        return f"Erro: {requisicao.status_code}"    
    
def criarRegistro(titulo, corpo, usuario_id):

    body = {
        "title": titulo,
        "body": corpo,
        "userId": usuario_id
    }

    dados = {
        'url': 'https://jsonplaceholder.typicode.com/posts',
        'method': 'POST',
        'body': str(body).replace("'", '"'),  # Convertendo para JSON
        # 'body': '{"title": "' + titulo + '", "body": "' + corpo + '", "userId": ' + usuario_id + '}',
        'headers': {
            'Content-type': 'application/json; charset=UTF-8',
        },
    }
    try:
        resposta = requests.post(dados['url'], data=dados['body'], headers=dados['headers'])
        if resposta.status_code == 200 or resposta.status_code == 201:
            return resposta.text
        else:
            return f"Erro: {resposta.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Erro ao fazer a requisição: {e}"

def atualizarRegistro(registro, titulo, corpo, usuario_id):
    body = {
        "title": titulo,
        "body": corpo,
        "userId": usuario_id
    }

    dados = {
        'url': 'https://jsonplaceholder.typicode.com/posts/' + str(registro),
        'method': 'PUT',
        'body': str(body).replace("'", '"'),  # Convertendo para JSON
        'headers': {
            'Content-type': 'application/json; charset=UTF-8',
        },
    }
    try:
        resposta = requests.put(dados['url'], data=dados['body'], headers=dados['headers'])
        if resposta.status_code == 200:
            return resposta.text
        else:
            return f"Erro: {resposta.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Erro ao fazer a requisição: {e}"

def atualizarParcialRegistro(registro, titulo=None, corpo=None, usuario_id=None):
    
    body = {}
    if titulo is not None:
        body["title"] = titulo
    if corpo is not None:
        body["body"] = corpo
    if usuario_id is not None:
        body["userId"] = usuario_id

    dados = {
        'url': 'https://jsonplaceholder.typicode.com/posts/' + str(registro),
        'method': 'PATCH',
        'body': str(body).replace("'", '"'),  # Convertendo para JSON
        'headers': {
            'Content-type': 'application/json; charset=UTF-8',
        },
    }
    try:
        resposta = requests.patch(dados['url'], data=dados['body'], headers=dados['headers'])
        if resposta.status_code == 200:
            return resposta.text
        else:
            return f"Erro: {resposta.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Erro ao fazer a requisição: {e}"
    
def excluirRegistro(registro):
    dados = {
        'url': 'https://jsonplaceholder.typicode.com/posts/' + str(registro),
        'method': 'DELETE',
        'headers': {
            'Content-type': 'application/json; charset=UTF-8',
        },
    }
    try:
        resposta = requests.delete(dados['url'], headers=dados['headers'])
        if resposta.status_code == 200 or resposta.status_code == 204:
            return "Registro excluído com sucesso."
        else:
            return f"Erro: {resposta.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Erro ao fazer a requisição: {e}"
    
def main():

    # Exemplo de uso da função metodoGET
    # registro = input("Digite o ID do registro: ")
    # conteudo = listarRegistro(registro)
    # print(conteudo)

    #print(listarTudo())

    # print("Criando um novo registro...")
    # titulo = "titulo1"
    # corpo = "corpo1"
    # usuario_id = 1
    # resposta = criarRegistro(titulo, corpo, usuario_id)
    # print(resposta)

    # print("Atualizando um registro...")
    # registro = 1
    # titulo = "titulo atualizado"
    # corpo = "corpo atualizado"  
    # usuario_id = 1
    # resposta = atualizarRegistro(registro, titulo, corpo, usuario_id)
    # print(resposta)
    
    # print("Atualizando parcialmente um registro...")
    # registro = 1      
    # usuario_id = 1
    # resposta = atualizarParcialRegistro(registro, usuario_id)        
    # print(resposta)

    print("Excluindo um registro...")
    registro = 1    
    resposta = excluirRegistro(registro)
    print(resposta)

main()