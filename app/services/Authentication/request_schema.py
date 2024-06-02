from pydantic import BaseModel, Field
from datetime import date
class CreateUser(BaseModel):
    username: str = Field(default="JohnDoe08", description="Username that user had", max_length=50)
    email: str = Field(default="johndoe88@gmail.com", description="User's valid email", max_length=255)
    password: str = Field(default=None, description="User's password", max_length=255)
    name: str = Field(default="John", description="User's name", max_length=100)
    dob: date = Field(default=date.today(), description="User's birthday date")
    gender: str = Field("Male")