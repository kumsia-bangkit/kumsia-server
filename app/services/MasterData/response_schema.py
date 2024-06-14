from pydantic import BaseModel
from typing import List, Optional

class HobbyList(BaseModel):
    Hobbies: Optional[List]

class CityList(BaseModel):
    Cities: Optional[List]