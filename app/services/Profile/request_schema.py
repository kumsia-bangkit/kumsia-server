from pydantic import BaseModel, Field
from app.enums.enum import Gender, Religion
from datetime import date
class UpdateProfile(BaseModel):
    username: str = Field(default="john_doe", description="New user's username")
    name: str = Field(default="John Alexander", description="New user's name")
    email: str = Field(default="john.alexander@gmail.com", description="New user's email")
    contact: str = Field(default="08121283981", description="New user's contact")
    guardian_contact: str = Field(default="08121283981", description="New user's guardian contact")
    # profile_picture: str = Field(description="Contain images for user's prfoile picture")
    religion: Gender = Field(description="Requested religion changes")
    gender: Religion = Field(description="Requested gender changes")
    dob: date = Field(default=date.today(), description="User's birthday date")
    city: str = Field(default="Kota Tangerang", description="User's chosen city")