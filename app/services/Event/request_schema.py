import json
from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional
from app.enums.event import Type
from app.enums.gender import Gender

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

class Event(BaseModel):
    name: Optional[str]
    location: Optional[str]
    type: Optional[Type]
    event_start: Optional[datetime]
    city: Optional[str]
    link: Optional[str]
    description: Optional[str]
    attendee_criteria: Optional[str]
    contact: Optional[str]
    capacity: Optional[int]
    hobby_preference: Optional[list]
    religion_preference: Optional[list]
    city_preference: Optional[list]
    gender_preference: Optional[list[Gender]]

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
