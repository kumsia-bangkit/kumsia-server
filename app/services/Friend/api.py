from typing import Annotated
from fastapi import APIRouter, Header
from app.utils.authentication import validate_token_and_id
from . import response_schema, service as FriendService

friend_router = APIRouter(prefix="/friends", tags=['Friends'])

@friend_router.get('/', response_model=response_schema.FriendList)
async def get_friends(access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return FriendService.get_friends(user_id)

@friend_router.get('/request', response_model=response_schema.FriendList)
async def get_friend_requests(access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return FriendService.get_friend_req(user_id)

@friend_router.post('/send')
async def send_request(friend_id: str, access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return FriendService.send_friend_req(friend_id, user_id)

@friend_router.put('/accept')
async def accept_request(friend_id: str, access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return FriendService.accept_friend_req(friend_id, user_id)

@friend_router.delete('/reject')
async def reject_request(friend_id: str, access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return FriendService.reject_friend_req(friend_id, user_id)