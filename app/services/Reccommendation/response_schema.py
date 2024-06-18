from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    user_id: Optional[str]
    username: Optional[str]
    name: Optional[str]
    profile_picture: Optional[str]
    religion: Optional[str]
    gender: Optional[str]
    city: Optional[str]

class UsersList(BaseModel):
    users: Optional[List[User]]