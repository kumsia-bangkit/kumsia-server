from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from app.utils.authentication import authenticate_user, create_access_token, get_current_user
from . import response_schema, request_schema, service as AuthService
from app.utils.utility import update_last_activity

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
auth_router = APIRouter()

@auth_router.post("/login", tags=['Authentication'], response_model=response_schema.Login)
async def login_for_access_token(request: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_data = authenticate_user(request.username, request.password)
    # Check if user_data return Response
    if isinstance(user_data, JSONResponse):
        return user_data
    token = create_access_token(user_data[0], user_data[1])
    update_last_activity(user_data[0]['sub'])
    return response_schema.Login(access_token=token)

@auth_router.post('/register', tags=['Authentication'])
async def register(request: request_schema.CreateUser):
    register_response = AuthService.register(request)
    return register_response

@auth_router.post('/register/organization', tags=['Authentication'])
async def register_organization(request: request_schema.CreateOrganization):
    register_organization_response = AuthService.register_organization(request)
    return register_organization_response

@auth_router.get('/users', tags=['Authentication'], response_model=response_schema.User)
async def get_users(token: Annotated[str, Header()]):
    user_data = get_current_user(token)
    return response_schema.User(user=user_data)
