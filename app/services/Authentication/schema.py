from uuid import UUID
from pydantic import BaseModel

class Individual(BaseModel):
    id: UUID

class Organization(BaseModel):
    id: UUID