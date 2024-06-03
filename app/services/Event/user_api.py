from fastapi import APIRouter
from . import response_schema, user_service as EventService

user_event_router = APIRouter(prefix="/events/user", tags=['Event User'])

@user_event_router.get('/all', response_model=response_schema.UserEventList)
async def get_events():
    return EventService.get_all()

@user_event_router.get('/joined', response_model=response_schema.UserEventList)
async def get_joined_events():
    return EventService.get_all_joined_event()

@user_event_router.get('/{event_id}', response_model=response_schema.UserEvent)
async def get_event_by_id(event_id: str):
    return EventService.get_event_by_id(event_id)

@user_event_router.post('/join', response_model=response_schema.UserEvent)
async def join_event(event_id: str):
    return EventService.join_event(event_id)

@user_event_router.delete('/unjoin', response_model=response_schema.UserEvent)
async def unjoin_event(event_id: str):
    return EventService.cancel_join_event(event_id)