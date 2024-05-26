from uuid import UUID, uuid4
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enums.gender import Gender
from enums.event_status import Status
from services.Authentication.schema import Individual, Organization

class Event(BaseModel):
    # id: Optional[UUID] = uuid4()
    city: Optional[str]
    capacity: Optional[int]
    contact_link: Optional[str]
    date_time: Optional[datetime]
    description: Optional[str]
    disclaimer: Optional[str]
    gender_restriction: Optional[Gender]
    # last_edited: Optional[datetime]
    location: Optional[str]
    name: Optional[str]
    # organizer: Optional[Organization]
    # status: Optional[Status]
