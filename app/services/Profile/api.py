from fastapi import APIRouter, File, Header, UploadFile
from fastapi.responses import JSONResponse
from . import request_schema as Request, service as ProfileServices
from app.services.gcs import GCStorage
from typing import Annotated
from app.utils.authentication import validate_token_and_id, validate_token

profile_router = APIRouter()

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/gif"}

@profile_router.get('/profile', tags=['Profile'])
async def get_profile(access_token: Annotated[str, Header(description="User valied access token to access the services")]):
    id = validate_token_and_id(access_token)
    get_profile_response = ProfileServices.get_user_profile(id)
    return get_profile_response

@profile_router.patch('/profile', tags=['Profile'])
async def update_profile(
    request: Request.UpdateProfile, 
    access_token: Annotated[str, Header(description="User valied access token to access the services")],
    file:UploadFile = File(None)
):
    payload = validate_token(access_token)

    file_path = None
    if file:
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            return JSONResponse({"message": "Invalid file type. Only JPEG, JPG, PNG, and GIF files are allowed."}, status_code=400)
    
        file_path = GCStorage().upload_file(file)

    update_profile_response = ProfileServices.update_user_profile(request, payload.get("sub"), payload.get("username"), file_path)
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
    access_token: Annotated[str, Header(description="User valied access token to access the services")],
    file: UploadFile = File(None)
):
    payload = validate_token(access_token)

    file_path = None
    if file:
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            return JSONResponse({"message": "Invalid file type. Only JPEG, JPG, PNG, and GIF files are allowed."}, status_code=400)
    
        file_path = GCStorage().upload_file(file)

    update_profile_response = ProfileServices.update_org_profile(request, payload.get("sub"), payload.get("username"), file_path)
    return update_profile_response

@profile_router.delete('/organization/profile', tags=['Profile'])
async def delete_org_profile(
    access_token: Annotated[str, Header(description="User valied access token to access the services")]
):
    id = validate_token_and_id(access_token)
    delete_profile_response = ProfileServices.delete_org_profile(id)
    return delete_profile_response
