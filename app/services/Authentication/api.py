from fastapi import APIRouter, Depends
from typing import Annotated
from . import response_schema, request_schema, service as AuthService
from utils.authentication import authenticate_user

auth_router = APIRouter()

@auth_router.post('/register', tags=['Authentication'], response_model=response_schema.UserCreated)
async def register(request: request_schema.CreateUser):
    register_response = AuthService.register(request)
    return register_response