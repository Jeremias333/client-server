from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import json
from pydantic import BaseSettings
import functions as func
import uvicorn


class Settings(BaseSettings):
    app_name: str = "Servidor"
    port_default: int = 3301

settings = Settings()
app = FastAPI()

print("       SERVICE: {}".format(settings.app_name))

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "*"]
)

@app.get("/")
def route_index():
    content = func.get_content_instructions()
    return JSONResponse(status_code=200, content={
        "message": content,
        "status_code": 200,
    })

@app.get("/test/")
def route_test():
    try:
        return JSONResponse(status_code=200, content={
            "message": "Você está na rota teste",
            "status_code": 200,
        })
    except ValueError as e:
        return JSONResponse(status_code=500, content={
            "message": "Você está na rota teste, porém ocorreu um erro",
            "status_code": 500,
        })

@app.post("/test/")
async def route_post_test(request: Request):
    try:
        body = await request.body()
        body = json.loads(body)
        return JSONResponse(status_code=200, content={
            "message": "Você está na rota teste, do tipo post, com o body: {}".format(body),
            "status_code": 200,
        })
    except ValueError as e:
        return JSONResponse(status_code=500, content={
            "message": "Você está na rota teste, porém ocorreu um erro",
            "status_code": 500,
        })

@app.post("/send/message/")
async def route_send_message(request: Request):
    try:
        body = await request.body()
        body = json.loads(body)
        
        print("Estrutura que recebi: {}\n".format(body))

        if(func.verify_data_structure_passkey(body)):
            passkey = body["passkey"]

        if (body["duplicated"] == True):
            build_message = "Erro ao ler mensagem pois está duplicada"

            message_decrypt = func.decrypt_message(body["message"], passkey)
            message_decrypt = message_decrypt.replace("'", "\"")

            print("Mensagem recebida decriptada: {}\n".format(message_decrypt))

            message_dict = dict()
            message_dict["message"] = eval(message_decrypt)
            
            message_dict["message"]["text"] = build_message

            message_encrypt = func.encrypt_message(str(message_dict["message"]), passkey)
            response_content = {
                "message": message_encrypt,
                "passkey": passkey,
                "duplicated": True
            }
            
            print("Preparando mensagem: {}\n".format(response_content))
            
            response_content = json.dumps(response_content)
            
            return JSONResponse(status_code=200, content=response_content)

        message_decrypt = func.decrypt_message(body["message"], passkey)
        message_decrypt = message_decrypt.replace("'", "\"")

        print("Mensagem recebida decriptada: {}\n".format(message_decrypt))

        message_dict = dict()
        message_dict["message"] = eval(message_decrypt)

        if(func.verify_data_structure_message(message_dict)):
            message = message_dict["message"]

        #Processar mensagem
        response_message_decrypt = func.process_message(message, passkey)

        #Encriptar mensagem
        response_message_encrypt = func.encrypt_message(response_message_decrypt, passkey)

        #Responder
        response_content = {
            "message": response_message_encrypt,
            "passkey": passkey,
        }
        
        response_content = json.dumps(response_content)

        #response = "{}".format(body)
        return JSONResponse(status_code=200, content=response_content)
    except ValueError as e:
        return JSONResponse(status_code=500, content={
            "message": "Você está na rota /send/message/, porém ocorreu um erro: {}".format(e),
            "status_code": 500,
        })


if __name__ == "__main__":
    uvicorn.run("server:app", reload=True, host="0.0.0.0", port=settings.port_default)