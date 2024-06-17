from pydantic import BaseModel, Field
from app.enums.enum import Gender, Religion
from datetime import date
from typing import Optional
class UpdateProfile(BaseModel):
    username: str = Field(None, examples=['john_doe'], description="New user's username")
    name: str = Field(None, examples=['John Alexander'], description="New user's name")
    email: str = Field(None, examples=['john.alexander@gmail.com'], description="New user's email")
    contact: str = Field(None, examples=['08121283981'], description="New user's contact")
    guardian_contact: str = Field(None, examples=['08121283981'], description="New user's guardian contact")
    # profile_picture: str = Field(description="Contain images for user's profile picture")
    religion: Gender = Field(None, examples=[Gender.Male], description="Requested religion changes")
    gender: Religion = Field(None, examples=[Religion.Hindu], description="Requested gender changes")
    dob: date = Field(None, examples=['2000-01-01'], description="User's birthday date")
    city: str = Field(None, examples=['Kota Tangerang'], description="User's chosen city")
    hobby_preference: Optional[list]
    religion_preference: Optional[list]
    city_preference: Optional[list]
    gender_preference: Optional[list[Gender]]

class UpdateOrgProfile(BaseModel):
    name: str = Field(None, examples=['John Alexander'], description="New user's name")
    username: str = Field(None, examples=['john_doe'], description="New user's username")
    email: str = Field(None, examples=['john.alexander@gmail.com'], description="New user's email")
    # profile_picture: str = Field(description="Contain images for user's profile picture")
    description: str = Field(None, examples=['Organization Examples'], description="Organization description")
    contact: str = Field(None, examples=['08121283981'], description="New user's contact")
    
class Preference(BaseModel):
    hobby: Optional[list]
    religion: Optional[list]
    city: Optional[list]
    gender: Optional[list[Gender]]