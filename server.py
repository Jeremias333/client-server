from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import json
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Servidor"
    port_default: int = 8000

settings = Settings()
app = FastAPI()

print("       SERVICE: {}".format(settings.app_name))

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "*"]
)

@app.get("/test/")
def route_test():
    try:
        return JSONResponse(status_code=200, content={
            "message": "Você está na rota teste",
            "status_code": 200,
            "flag": True
        })
    except ValueError as e:
        return JSONResponse(status_code=500, content={
            "message": "Você está na rota teste, porém ocorreu um erro",
            "status_code": 500,
            "flag": True
        })

@app.post("/test/")
async def route_post_test(request: Request):
    try:
        body = await request.body()
        body = json.loads(body)
        return JSONResponse(status_code=200, content={
            "message": "Você está na rota teste, do tipo post, com o body: {}".format(body),
            "status_code": 200,
            "flag": True
        })
    except ValueError as e:
        return JSONResponse(status_code=500, content={
            "message": "Você está na rota teste, porém ocorreu um erro",
            "status_code": 500,
            "flag": True
        })

@app.post("/div/")
async def route_div(request: Request):
    try:
        body = await request.body()
        body = json.loads(body)
        caso_test = 0

        if int('value_a' in body.keys()):
            caso_test += 1
        
        if int('value_c' in body.keys()):
            caso_test += 1
        
        if caso_test < 2:
            raise ValueError("Pacote não está de acordo com o protocolo (regra)")

        result = int(body["value_a"]) / int(body["value_c"])
        
        return JSONResponse(status_code=200, content={
            "message": "O resultado da divisão é: {}".format(result),
            "status_code": 200,
            "flag": True
        })
    except ValueError as e:
        return JSONResponse(status_code=500, content={
            "message": "Você está na rota de divisão, porém ocorreu um erro: {}".format(e),
            "status_code": 500,
            "flag": True
        })

@app.post("/route/2")
async def route_2(request: Request):
    try:
        body = await request.body()
        body = json.loads(body)

        return JSONResponse(status_code=200, content={
            "message": body
        })
    except ValueError as e:

        return JSONResponse(status_code=500, content={
            "msg":"Ocorreu um erro: {}".format(e)
        })

