from fastapi import APIRouter, Header
from . import response_schema as Response, request_schema as Request, service as ProfileServices
from typing import Annotated
from app.utils.authentication import validate_token_and_id

profile_router = APIRouter()

@profile_router.get('/profile', tags=['Profile'])
async def get_profile(access_token: Annotated[str, Header(description="User valied access token to access the services")]):
    id = validate_token_and_id(access_token)
    get_profile_response = ProfileServices.get_user_profile(id)
    return get_profile_response

@profile_router.patch('/profile', tags=['Profile'], response_model=Response.ProfileUpdated)
async def update_profile(
    request: Request.UpdateProfile, 
    access_token: Annotated[str, Header(description="User valied access token to access the services")]
):
    id = validate_token_and_id(access_token)
    update_profile_response = ProfileServices.update_user_profile(request, id)
    return update_profile_response

@profile_router.delete('/profile', tags=['Profile'])
async def delete_profile(
    access_token: Annotated[str, Header(description="User valied access token to access the services")]
):
    id = validate_token_and_id(access_token)
    delete_profile_response = ProfileServices.delete_profile(id)
    return delete_profile_response

@profile_router.get('/organization/profile', tags=['Profile'])
async def get_org_profile(access_token: Annotated[str, Header(description="User valied access token to access the services")]):
    id = validate_token_and_id(access_token)
    get_profile_response = ProfileServices.get_org_profile(id)
    return get_profile_response

@profile_router.patch('/organization/profile', tags=['Profile'])
async def update_org_profile(
    request: Request.UpdateOrgProfile, 
    access_token: Annotated[str, Header(description="User valied access token to access the services")]
):
    id = validate_token_and_id(access_token)
    update_profile_response = ProfileServices.update_org_profile(request, id)
    return update_profile_response

@profile_router.delete('/organization/profile', tags=['Profile'])
async def delete_org_profile(
    access_token: Annotated[str, Header(description="User valied access token to access the services")]
):
    id = validate_token_and_id(access_token)
    delete_profile_response = ProfileServices.delete_org_profile(id)
    return delete_profile_response
