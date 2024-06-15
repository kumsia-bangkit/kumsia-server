from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.enums.event import Type, Status
from app.enums.gender import Gender
    
class OrganizationEvent(BaseModel):
    event_id: Optional[str]
    organization_id: Optional[str]
    name: Optional[str]
    location: Optional[str]
    profie_picture: Optional[str]
    status: Optional[Status]
    type: Optional[Type]
    event_start: Optional[datetime]
    city: Optional[str]
    link: Optional[str]
    description: Optional[str]
    attendee_criteria: Optional[str]
    contact_varchar: Optional[str]
    like_count: Optional[int]
    capacity: Optional[int]
    last_edited: Optional[datetime]
    preference_id: Optional[str]
    hobby_preference: Optional[list]
    religion_preference: Optional[list]
    city_preference: Optional[list]
    gender_preference: Optional[list[Gender]]


class OrganizationEventList(BaseModel):
    events: Optional[List[OrganizationEvent]]

class UserEvent(BaseModel):
    event_id: Optional[str]
    organization_id: Optional[str]
    name: Optional[str]
    location: Optional[str]
    profie_picture: Optional[str]
    status: Optional[Status]
    type: Optional[Type]
    event_start: Optional[datetime]
    city: Optional[str]
    link: Optional[str]
    description: Optional[str]
    attendee_criteria: Optional[str]
    contact_varchar: Optional[str]
    like_count: Optional[int]
    capacity: Optional[int]
    last_edited: Optional[datetime]
    joined: Optional[bool]
    liked: Optional[bool]
    preference_id: Optional[str]
    hobby_preference: Optional[list]
    religion_preference: Optional[list]
    city_preference: Optional[list]
    gender_preference: Optional[list[Gender]]

class UserEventList(BaseModel):
    events: Optional[List[UserEvent]]
