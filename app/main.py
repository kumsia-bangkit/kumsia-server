from fastapi import FastAPI
from services.Authentication.api import auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.services.Event.org_api import org_event_router
from app.services.Event.user_api import user_event_router

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
app.include_router(org_event_router)
app.include_router(user_event_router)

@app.get("/")
def read_hello():
    return {"Hello": "World"}