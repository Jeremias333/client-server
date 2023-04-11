import requests
import json
import functions as func

url_base = 'http://127.0.0.1:3301'

def index():
    url = url_base + '/'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url)
    
    print(response.json())

def test_server():
    url = url_base + '/test/'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url)
    
    print(response.json())

def test_server_post():
    url = url_base + '/test/'
    headers = {'Content-Type': 'application/json'}
    body = {
        "name": "Pedro",
        "age": 19,
    }
    response = requests.post(url, json=body, headers=headers)
    
    print(response.json())

def send_message(
    text = "Exemplo de texto",
    error = False,
    lost = False,
    npackages = 1,
    multpackages = False,
    passkey = "3302",
    duplicated = False
):
    url = url_base + '/send/message/'
    headers = {'Content-Type': 'application/json'}
    passkey = passkey
    message_attr ={
    "text": text,
    "error": error,
    "lost": lost,
    "npackages": npackages,
    "multpackages": multpackages,
    }

    message_attr = str(message_attr)

    encrypt_message = func.encrypt_message(message_attr, passkey)

    decrypt_json = json.dumps(func.decrypt_message(encrypt_message, passkey))

    body = {
        "message": encrypt_message,
        "passkey": passkey,
        "duplicated": duplicated,
    }

    print("Entrada enviada para o servidor: {}\n".format(body))

    response = requests.post(url, json=body, headers=headers)

    message_dict = json.loads(response.json())
 
    print("Resposta do servidor: {}\n".format(message_dict))
    print("Iniciando processo de descriptografia da mensagem recebida do servidor\n")

    message_decrypt = func.decrypt_message(message_dict["message"], passkey)

    print("Resposta do Servidor: {}\n".format(message_decrypt))
    print("Apenas a mensagem resposta do servidor - {}".format(eval(message_decrypt)["text"]))

def teste_conexao():
    index()

def enviar_mensagem_padrao():
    send_message()

def enviar_mensagem_padrao_com_perdas():
    send_message(lost=True)

def enviar_mensagem_padrao_com_erros():
    send_message(error=True)

def enviar_mensagem_por_pacotes():
    send_message(text=["nov","em","bro"], multpackages=True, npackages=3)

def enviar_mensagem_por_pacotes_com_perdas():
    send_message(text=["nov","em","bro"], multpackages=True, npackages=3, lost=True)

def enviar_mensagem_por_pacotes_com_erros():
    send_message(text=["nov","em","bro"], multpackages=True, npackages=3, error=True)

def enviar_mensagem_duplicada():
    send_message(duplicated=True)

def sair():
    print("Saindo...")
    exit()

while True:
    print("Selecione uma opção:")
    print("1 - Teste de conexão")
    print("2 - Enviar mensagem padrão")
    print("3 - Enviar mensagem padrão com erros")
    print("4 - Enviar mensagem padrão com perdas")
    print("5 - Enviar mensagem por pacotes")
    print("6 - Enviar mensagem por pacotes com perdas")
    print("7 - Enviar mensagem por pacotes com erros")
    print("8 - Enviar mensagem duplicada")
    print("9 - Sair")

    opcao = input()

    if opcao == '1':
        teste_conexao()
    elif opcao == '2':
        enviar_mensagem_padrao()
    elif opcao == '3':
        enviar_mensagem_padrao_com_erros()
    elif opcao == '4':
        enviar_mensagem_padrao_com_perdas()
    elif opcao == '5':
        enviar_mensagem_por_pacotes()
    elif opcao == '6':
        enviar_mensagem_por_pacotes_com_perdas()
    elif opcao == '7':
        enviar_mensagem_por_pacotes_com_erros()
    elif opcao == '8':
        enviar_mensagem_duplicada()
    elif opcao == '9':
        sair()
    else:
        print("Opção inválida. Tente novamente.")


