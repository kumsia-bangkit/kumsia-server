from pydantic import BaseModel, Field
class UpdateProfile(BaseModel):
    username: str = Field(default="john_doe", description="New user's username")
    name: str = Field(default="John Alexander", description="New user's name")
    email: str = Field(default="john.alexander@gmail.com", description="New user's email")
    contact: str = Field(default="08121283981", description="New user's contact")