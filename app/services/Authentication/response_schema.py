from pydantic import BaseModel

class Login(BaseModel):
    # JWT Response
    access_token: str