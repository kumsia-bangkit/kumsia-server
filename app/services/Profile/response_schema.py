from pydantic import BaseModel, Field
class ProfileUpdated(BaseModel):
    message: str = Field(description="Message given after profile updated")