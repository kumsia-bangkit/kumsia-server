from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    password: str
    dob: str
    account_type: str