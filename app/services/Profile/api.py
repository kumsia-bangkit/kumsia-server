from fastapi import APIRouter, File, Header, UploadFile
from fastapi.responses import JSONResponse
from . import response_schema as response, request_schema as Request, service as ProfileServices
from app.services.gcs import GCStorage
from typing import Annotated
from app.utils.authentication import validate_token_and_id, validate_token

profile_router = APIRouter(prefix="/profile", tags=['Profile'])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/gif"}

@profile_router.get('/user', response_model=response.ProfileDetail)
async def get_profile(access_token: Annotated[str, Header(description="User valid access token to access the services")]):
    id = validate_token_and_id(access_token)
    get_profile_response = ProfileServices.get_profile(id)
    return get_profile_response

@profile_router.get('/user/{user_id}', response_model=response.ProfileDetail)
async def get_other_profile(user_id: str, access_token: Annotated[str, Header(description="User valid access token to access the services")]):
    payload = validate_token(access_token)
    return ProfileServices.get_user_profile(user_id, payload.get("sub"), payload.get("role"))

@profile_router.patch('/user/update', response_model=response.Token)
async def update_profile(
    request: Request.UpdateProfile, 
    access_token: Annotated[str, Header(description="User valid access token to access the services")],
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

@profile_router.delete('/user/delete')
async def delete_profile(
    access_token: Annotated[str, Header(description="User valid access token to access the services")]
):
    id = validate_token_and_id(access_token)
    delete_profile_response = ProfileServices.delete_profile(id)
    return delete_profile_response

@profile_router.get('/organization', response_model=response.OrganizationDetail)
async def get_org_profile(access_token: Annotated[str, Header(description="User valid access token to access the services")]):
    id = validate_token_and_id(access_token)
    get_profile_response = ProfileServices.get_org_profile(id)
    return get_profile_response

@profile_router.get('/organization/{organization_id}', response_model=response.OrganizationDetail)
async def get_other_org_profile(organization_id: str, access_token: Annotated[str, Header(description="User valid access token to access the services")]):
    validate_token(access_token)
    return ProfileServices.get_org_profile(organization_id)

@profile_router.patch('/organization/update', response_model=response.Token)
async def update_org_profile(
    request: Request.UpdateOrgProfile, 
    access_token: Annotated[str, Header(description="User valid access token to access the services")],
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

@profile_router.delete('/organization/delete')
async def delete_org_profile(
    access_token: Annotated[str, Header(description="User valid access token to access the services")]
):
    id = validate_token_and_id(access_token)
    delete_profile_response = ProfileServices.delete_org_profile(id)
    return delete_profile_response
