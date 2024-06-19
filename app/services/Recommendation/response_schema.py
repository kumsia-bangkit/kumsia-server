from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.enums.event import Status, Type
from app.enums.gender import Gender

class User(BaseModel):
    user_id: Optional[str]
    username: Optional[str]
    name: Optional[str]
    dob: Optional[str]
    profile_picture: Optional[str]
    religion: Optional[str]
    gender: Optional[str]
    city: Optional[str]
    hobbies: Optional[List[str]]

class Event(BaseModel):
    event_id: Optional[str]
    organization_id: Optional[str]
    organization_name: Optional[str]
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

class UsersList(BaseModel):
    users: Optional[List[User]]

class EventList(BaseModel):
    events: Optional[List[Event]]