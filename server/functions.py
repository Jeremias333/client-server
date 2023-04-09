try:
    import sys
    import os
    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '../'
            )
        )
    )
except:
    raise

import uuid
import hashlib
from package import Package

def get_content_instructions():
    text = """
          - Conexão com o servidor efetuada com sucesso!
          - É possível enviar mensagens para o servidor

          - Cada mensagem é tratada como um pacote de dados
          - É possível enviar mais de um pacote de dados por vez
          - Dependendo da flag passada você irá receber respostas diferentes

          - Os atributos precisam estar em JSON e deverão ser passado no body da requisição da rota: /send/package/
          - Atributos:
            - message: 
                - text: "string" ou ["string"]
                - error: boolean
                - lost: boolean
                - npackages: int
                - multpackages: boolean
            - passkey: "string"
    """
    return text

def get_unique_id():
    return str(uuid.uuid4())

def encrypt_message(message: str() or [str()] = "", passkey: str() = "3301"):
    # Generate a key from the hash value
    key = hashlib.sha256(passkey.encode()).digest()

    # Convert the text to bytes
    text_bytes = message.encode()

    # Encrypt the text with the key and convert to hexadecimal
    encrypted_text_bytes = bytearray()
    for i in range(0, len(text_bytes), len(key)):
        block = text_bytes[i:i+len(key)]
        if len(block) < len(key):
            block += b'\0' * (len(key) - len(block))
        encrypted_text_bytes += bytes([a ^ b for a, b in zip(block, key)])
    encrypted_text_hex = encrypted_text_bytes.hex()

    return encrypted_text_hex

def decrypt_message(message: str() or [str()] = "", passkey: str() = "3301"):
     # Generate a key from the hash value
    key = hashlib.sha256(passkey.encode()).digest()

    # Decrypt the text to bytes from the hexadecimal
    encrypted_text_bytes = bytes.fromhex(message)
    decrypted_text_bytes = bytearray()
    for i in range(0, len(encrypted_text_bytes), len(key)):
        block = encrypted_text_bytes[i:i+len(key)]
        decrypted_text_bytes += bytes([a ^ b for a, b in zip(block, key)])
    decrypted_text = decrypted_text_bytes.rstrip(b'\0').decode()

    return decrypted_text

def verify_data_structure_message(body: dict()):
    if (body["message"]["text"] == None or "text" not in body["message"].keys()):
        raise ValueError("Atributo message.text não foi passado")
    if (body["message"]["error"] == None or "error" not in body["message"].keys()):
        raise ValueError("Atributo message.error não foi passado")
    if (body["message"]["lost"] == None or "lost" not in body["message"].keys()):
        raise ValueError("Atributo message.lost não foi passado")
    if (body["message"]["npackages"] == None or "npackages" not in body["message"].keys()):
        raise ValueError("Atributo message.npackages não foi passado")
    if (body["message"]["multpackages"] == None or "multpackages" not in body["message"].keys()):
        raise ValueError("Atributo message.multpackages não foi passado")
    return True

def verify_data_structure_passkey(body: dict()):
    if (body["passkey"] == None or "passkey" not in body.keys()):
        raise ValueError("Atributo passkey não foi passado")
    return True

def process_message(message: dict(), passkey: str()):
    response_message = dict()

    text = ""
    #processamento da mensagem
    package = Package(
        id=get_unique_id(),
        text=message["text"],
        error=message["error"],
        lost=message["lost"],
        npackages=message["npackages"],
        multpackages=message["multpackages"],
        passkey=passkey
    )
    try:
        if package.npackages == 1:
            if (package.error):
                text = "Ocorreu um erro no processamento da mensagem"
                raise ValueError("Mensagem com erro")

            if (package.lost):
                text = "Ocorreu perda no pacote enviado"
                raise ValueError("Mensagem perdida")
            
            if (package.multpackages):
                text = "Ocorreu um erro, foi passado que a mensagem teria mais de um pacote, porém foi passado apenas um"
                raise ValueError("Mensagem com mais de um pacote")
            
            text = "Mensagem recebida e processada com sucesso: {}".format(package.text)
        else:
            if (package.multpackages == True and package.npackages > 1 and type(package.text) == type(list())):
                text_append = ""
                for pkg in package.text:
                    text_append += pkg
                text = "Mensagem recebida e processada com sucesso: {}".format(text_append)
                
            if package.error == True:
                text = "Ocorreu um erro no processamento de um dos pacotes"
                raise ValueError("Mensagem com erro")

            if package.lost == True:
                text = "Ocorreu perda de um dos pacotes"
                raise ValueError("Mensagem perdida")

    except Exception as e:
        if text == "":
            response_message = {
                "id": package.id,
                "text": "Mensagem não atende ao protocolo de comunicação, por esse motivo não irá ser processada",
                "error": package.error,
                "lost": package.lost,
                "npackages": package.npackages,
                "multpackages": package.multpackages,
            }
        else:
            response_message = {
                "id": package.id,
                "text": text,
                "error": package.error,
                "lost": package.lost,
                "npackages": package.npackages,
                "multpackages": package.multpackages,
            }
            print("Retornando erro para Cliente")
        return str(response_message)

    response_message = {
        "id": package.id,
        "text": text,
        "error": package.error,
        "lost": package.lost,
        "npackages": package.npackages,
        "multpackages": package.multpackages,
    }

    print("Retornando mensagem sucesso para Cliente")
    return str(response_message)