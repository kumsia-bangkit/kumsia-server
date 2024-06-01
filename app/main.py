from fastapi import FastAPI
from app.services.Authentication.api import auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.services.Event.api import event_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router Extention
app.include_router(auth_router)
app.include_router(event_router)

@app.get("/")
def read_hello():
    return {"Hello": "World"}