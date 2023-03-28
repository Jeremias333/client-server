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

@app.get("/route/1")
def route_1():
    try:
        return JSONResponse(status_code=200, content={
            "message": "route1"
        })
    except ValueError as e:
        return JSONResponse(status_code=500, content={
            "msg":"Não consigo acessar a rota - {}".format(e)
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