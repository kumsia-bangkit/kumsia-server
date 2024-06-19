from typing import Annotated
from fastapi import APIRouter, Header
from app.utils.authentication import validate_token_and_id
from . import account_service as AccountService

recommendation_router = APIRouter(prefix="/recommend", tags=['recommend'])

@recommendation_router.get('/account')
async def get_recommendation(access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return AccountService.get_recommendation(user_id)