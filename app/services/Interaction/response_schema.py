from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class Comment(BaseModel):
    comment_id: Optional[str]
    user_id: Optional[str]
    user_name: Optional[str]
    user_picture: Optional[str]
    event_id: Optional[str]
    comment_text: Optional[str]
    created_at: Optional[datetime]


class CommentList(BaseModel):
    comments: Optional[List[Comment]]

class Like(BaseModel):
    event_id: Optional[str]
    user_id: Optional[str]
    is_liked: Optional[bool]