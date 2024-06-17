from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from app.enums.enum import Gender
class ProfileUpdated(BaseModel):
    message: Optional[str] = Field(None, description="Message given after profile updated")
    
class Preference(BaseModel):
    hobby: Optional[list]
    religion: Optional[list]
    city: Optional[list]
    gender: Optional[list[Gender]]
    
class ProfileDetail(BaseModel):
    user_id: Optional[str]
    username: Optional[str] = Field("default_username", description="The unique username of the user")
    name: Optional[str] = Field("John Doe", description="The full name of the user")
    email: Optional[str] = Field("default@example.com", description="The email address of the user")
    contact: Optional[str] = Field("0000000000", description="The contact number of the user")
    guardian_contact: Optional[str] = Field("1111111111", description="The contact number of the user's guardian")
    profile_picture: Optional[str] = Field("default_picture.jpg", description="URL to the user's profile picture")
    religion: Optional[str] = Field("Hindu", description="The religion of the user")
    gender: Optional[str] = Field("Male", description="The gender of the user")
    dob: Optional[str] = Field("User DOB", description="The date of birth of the user")
    city: Optional[str] = Field("Kota Bogor", description="The city where the user resides")
    last_activity: Optional[datetime] = Field(default_factory=datetime.utcnow, description="The timestamp of the user's last activity")
    preference: Optional[Preference]

class OrganizationDetail(BaseModel):
    organization_id: Optional[str]
    name: Optional[str] = Field("John Doe", description="The full name of the user")
    username: Optional[str] = Field("default_username", description="The unique username of the user")
    email: Optional[str] = Field("default@example.com", description="The email address of the user")
    profile_picture: Optional[str] = Field("default_picture.jpg", description="URL to the user's profile picture")
    description: Optional[str] = Field(None, examples=['Test Desc'])
    contact: Optional[str] = Field("0000000000", description="The contact number of the user")

class Token(BaseModel):
    # JWT Response
    access_token: str
