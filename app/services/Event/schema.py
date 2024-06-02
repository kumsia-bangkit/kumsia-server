from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enums.event_status import Status

class Preference(BaseModel):
    preference_id: Optional[str]
    hobby: Optional[list]
    religion: Optional[list]
    city: Optional[list]
    gender: Optional[list]

class Event(BaseModel):
    event_id: Optional[str]
    name: Optional[str]
    location: Optional[str]
    profile_picture: Optional[str]
    status: Optional[Status]
    type: Optional[str]
    date_time: Optional[datetime]
    city: Optional[str]
    link: Optional[str]
    description: Optional[str]
    attendee_criteria: Optional[str]
    contact: Optional[str]
    capacity: Optional[int]
    hobby: Optional[list]
    religion: Optional[list]
    city: Optional[list]
    gender: Optional[list]
