import json
from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional
from app.enums.event import Type
from app.enums.gender import Gender

class Comment(BaseModel):
    event_id: Optional[str]
    comment_text: Optional[str]

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value