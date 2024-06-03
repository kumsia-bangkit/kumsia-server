from fastapi import APIRouter, Header, Body
from . import response_schema, request_schema, service as ProfileServices
from typing import Annotated
from app.utils.authentication import validate_token_and_id

profile_router = APIRouter()

@profile_router.patch('/profile', tags=['Profile'])
async def update_profile(
    # request: request_schema.UpdateProfile, 
    access_token: Annotated[str, Header(description="User valied access token to access the services")]
):
    id = validate_token_and_id(access_token)
    return id