from pydantic import BaseModel
from typing import List, Optional
import datetime

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
    name: Optional[str]
    location: Optional[str]
    profile_picture: Optional[str]
    status: Optional[str]
    type: Optional[str]
    event_start: Optional[datetime.datetime]
    city: Optional[List[str]]
    link: Optional[str]
    description: Optional[str]
    attendee_criteria: Optional[str]
    contact_varchar: Optional[str]
    like_count: Optional[int]
    capacity: Optional[int]
    last_edited: Optional[datetime.datetime]

class UsersList(BaseModel):
    users: Optional[List[User]]

class EventList(BaseModel):
    events: Optional[List[Event]]