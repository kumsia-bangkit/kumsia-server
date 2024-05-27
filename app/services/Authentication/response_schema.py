from pydantic import BaseModel

class Login(BaseModel):
    # JWT Response
    token: str

class UserCreated(BaseModel):
    message: str