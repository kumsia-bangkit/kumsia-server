from fastapi import APIRouter
from . import response_schema, request_schema, service as AuthService

auth_router = APIRouter()

@auth_router.post('/register', tags=['Auth'], response_model=response_schema.UserCreated)
async def register(request: request_schema.CreateUser):
    register_response = AuthService.register(request)
    return register_response