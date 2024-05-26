from fastapi import FastAPI
from services.Authentication.api import auth_router
from services.Event.api import event_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(event_router)

@app.get("/")
def read_hello():
    return {"Hello": "World"}