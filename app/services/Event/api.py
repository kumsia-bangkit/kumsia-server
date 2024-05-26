from fastapi import APIRouter
from . import schema, service as EventService

event_router = APIRouter()

@event_router.get('/all', tags=['Event'])
async def get_events():
    return EventService.get_all()

@event_router.post('/new', tags=['Event'])
async def post_new_event(event: schema.Event):
    return EventService.post_event(event)