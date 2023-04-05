import requests
import json

url_base = 'http://127.0.0.1:8000'

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

def div(a, b):
    url = url_base + '/div/'
    headers = {'Content-Type': 'application/json'}
    body = {
        "value_a": a,
        "value_c": 10
    }
    response = requests.post(url, json=body, headers=headers)

    print(response.json())

def send_package(message: str() or [str()]):
    url = url_base + '/send/package/'
    headers = {'Content-Type': 'application/json'}
    body = {
        "message": message,
        "wanted": ["status", "response", "message_qtd"]
    }
    response = requests.post(url, json=body, headers=headers)
    
    
    print(response.json())


# print(send_message(["Messagem"]))

# test_server_post()

div(10, 3)