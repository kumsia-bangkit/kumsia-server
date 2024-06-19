from pydantic import BaseModel
from typing import List, Optional

class Friend(BaseModel):
    user_id: Optional[str]
    username: Optional[str]
    name: Optional[str]
    profile_picture: Optional[str]

class FriendList(BaseModel):
    friends: Optional[List[Friend]]