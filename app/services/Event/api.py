from fastapi import APIRouter, File, UploadFile
from . import schema, service as EventService
from app.services.gcs import GCStorage

event_router = APIRouter(prefix="/events", tags=['Event'])

@event_router.get('/all')
async def get_events():
    return EventService.get_all()

@event_router.get('/joined')
async def get_joined_events():
    return EventService.get_all_joined_event()

@event_router.get('/{event_id}')
async def get_event_by_id(event_id: str):
    return EventService.get_event_by_id(event_id)

@event_router.post('/new')
async def post_event(event: schema.Event, file:UploadFile=File(...)):
    if file:
        file_path = GCStorage().upload_file(file)
        event.profile_picture = file_path

    return EventService.post_event(event)

@event_router.put('/update')
async def update_event(event: schema.Event, file:UploadFile=File(...)):
    if file:
        file_path = GCStorage().upload_file(file)
        event.profile_picture = file_path

    return EventService.update_event(event)

@event_router.delete('/delete')
async def delete_event(event_id: str):
    return EventService.delete_event(event_id)

@event_router.put('/submit')
async def submit_event(event_id: str):
    return EventService.submit_event(event_id)

@event_router.put('/cancel')
async def cancel_event(event_id: str):
    return EventService.cancel_event(event_id)

@event_router.post('/join')
async def join_event(event_id: str):
    return EventService.join_event(event_id)

@event_router.delete('/unjoin')
async def unjoin_event(event_id: str):
    return EventService.cancel_join_event(event_id)