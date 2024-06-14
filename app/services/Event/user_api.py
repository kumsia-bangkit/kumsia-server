from typing import Annotated
from fastapi import APIRouter, Header

from app.utils.authentication import validate_token_and_id
from . import response_schema, user_service as EventService

user_event_router = APIRouter(prefix="/events/user", tags=['Event User'])

@user_event_router.get('/all', response_model=response_schema.UserEventList)
async def get_events(access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return EventService.get_all(user_id)

@user_event_router.get('/joined', response_model=response_schema.UserEventList)
async def get_joined_events(access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return EventService.get_all_joined_event(user_id)

@user_event_router.get('/liked', response_model=response_schema.UserEventList)
async def get_joined_events(access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return EventService.get_all_liked_event(user_id)

@user_event_router.get('/{event_id}', response_model=response_schema.UserEvent)
async def get_event_by_id(event_id: str, access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return EventService.get_event_by_id(event_id, user_id)

@user_event_router.post('/join', response_model=response_schema.UserEvent)
async def join_event(event_id: str, access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return EventService.join_event(event_id, user_id)

@user_event_router.delete('/unjoin', response_model=response_schema.UserEvent)
async def unjoin_event(event_id: str, access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return EventService.cancel_join_event(event_id, user_id)