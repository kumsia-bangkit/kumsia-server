from pydantic import BaseModel, Field
from typing import Union
from datetime import date

class CreateUser(BaseModel):
    username: str = Field("JohnDoe08")
    password: str
    first_name: str = Field("John")
    last_name: str = Field("Doe")
    dob: date
    roles: str = Field("User")
    gender: str = Field("Male")
    