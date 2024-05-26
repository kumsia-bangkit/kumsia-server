from pydantic import BaseModel

class Login(BaseModel):
    # JWT Response
    token: str