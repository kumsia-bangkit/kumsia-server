from typing import Annotated
from fastapi import APIRouter, Header
from app.utils.authentication import validate_token_and_id
from app.utils.utility import update_last_activity
from . import like_service as LikeService

like_router = APIRouter(prefix="/like", tags=['Like'])

@like_router.get('/is_liked')
async def get_is_liked(event_id: str, access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return LikeService.is_liked(event_id, user_id)

@like_router.post('/create')
async def like_event(event_id: str, access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    update_last_activity(user_id)
    return LikeService.post_like(event_id, user_id)

@like_router.delete('/delete')
async def unlike_event(event_id: str, access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    update_last_activity(user_id)
    return LikeService.delete_like(event_id, user_id)