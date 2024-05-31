from fastapi import FastAPI
from app.services.Authentication.api import auth_router

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
def read_hello():
    return {"Hello": "World"}