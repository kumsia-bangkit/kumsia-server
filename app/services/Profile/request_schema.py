import json
from pydantic import BaseModel, Field, model_validator
from app.enums.gender import Gender
from app.enums.religion import Religion
from datetime import date
from typing import Optional
class UpdateProfile(BaseModel):
    username: Optional[str] = Field(None, examples=['john_doe'], description="New user's username")
    name: Optional[str] = Field(None, examples=['John Alexander'], description="New user's name")
    email: Optional[str] = Field(None, examples=['john.alexander@gmail.com'], description="New user's email")
    contact: Optional[str] = Field(None, examples=['08121283981'], description="New user's contact")
    guardian_contact: Optional[str] = Field(None, examples=['08121283981'], description="New user's guardian contact")
    religion: Optional[Religion] = Field(None, examples=[Religion.HINDUISM], description="Requested religion changes")
    gender: Optional[Gender] = Field(None, examples=[Gender.MALE], description="Requested gender changes")
    dob: Optional[date] = Field(None, examples=['2000-01-01'], description="User's birthday date")
    city: Optional[str] = Field(None, examples=['Kota Tangerang'], description="User's chosen city")
    hobby_preference: Optional[list]
    religion_preference: Optional[list]
    city_preference: Optional[list]
    gender_preference: Optional[list[Gender]]
    new_password: Optional[str]
    password: Optional[str]

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

class UpdateOrgProfile(BaseModel):
    name: Optional[str] = Field(None, examples=['John Alexander'], description="New user's name")
    username: Optional[str] = Field(None, examples=['john_doe'], description="New user's username")
    email: Optional[str] = Field(None, examples=['john.alexander@gmail.com'], description="New user's email")
    description: Optional[str] = Field(None, examples=['Organization Examples'], description="Organization description")
    contact: Optional[str] = Field(None, examples=['08121283981'], description="New user's contact")

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
class Preference(BaseModel):
    hobby: Optional[list]
    religion: Optional[list]
    city: Optional[list]
    gender: Optional[list[Gender]]

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, list):
            return cls(**json.loads(value))
        return value