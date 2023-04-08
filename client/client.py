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

send_message()


