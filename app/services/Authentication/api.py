from fastapi import APIRouter
from . import schema, service as AuthService

auth_router = APIRouter()

@auth_router.get('/test', tags=['Auth'])
async def get_test():
    get_test_response = AuthService.get_test()
    return get_test_response