from pydantic import BaseModel, Field
from datetime import date
class CreateUser(BaseModel):
    username: str = Field(default="JohnDoe08", description="Username that user had", max_length=50)
    email: str = Field(default="johndoe88@gmail.com", description="User's valid email", max_length=255)
    password: str = Field(default=None, description="User's password", max_length=255)
    name: str = Field(default="John", description="User's name", max_length=100)
    dob: date = Field(default=date.today(), description="User's birthday date")
    gender: str = Field("Male")
class CreateOrganization(BaseModel):
    name: str = Field(default="John", description="Organization name", max_length=100)
    username: str = Field(default="JohnDoe08", description="Username that organization had", max_length=50)
    password: str = Field(default=None, description="Organization password", max_length=255)
    email: str = Field(default="johndoe88@gmail.com", description="Organization valid email", max_length=255)
