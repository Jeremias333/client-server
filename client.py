import requests

url_base = 'http://localhost:8000'

def send_message(message: str() or [str()] , act=0):
    url = url_base + '/route/1'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url)
    
    body_respose = {
        "message": response.json(),
        "status_code": response.status_code
    }
    return body_respose


print(send_message(["Messagem"]))