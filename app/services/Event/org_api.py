from fastapi import APIRouter, File, Form, UploadFile
from . import org_service as EventService, request_schema, response_schema
from app.services.gcs import GCStorage
from app.utils.authentication import validate_token_and_id

org_event_router = APIRouter(prefix="/events/org", tags=['Event Organization'])

@org_event_router.get('/all', response_model=response_schema.OrganizationEventList)
async def get_events(access_token: str):
    org_id = validate_token_and_id(access_token)
    return EventService.get_all(org_id)

@org_event_router.get('/{event_id}', response_model=response_schema.OrganizationEvent)
async def get_event_by_id(event_id: str, access_token: str):
    org_id = validate_token_and_id(access_token)
    return EventService.get_event_by_id(event_id, org_id)

@org_event_router.post('/new', response_model=response_schema.OrganizationEvent)
async def post_event(event:request_schema.Event=Form(...), file:UploadFile=File(...), access_token:str=Form(...)):
    org_id = validate_token_and_id(access_token)
    file_path = None
    if file:
        file_path = GCStorage().upload_file(file)
    return EventService.post_event(event, file_path, org_id)

@org_event_router.put('/update/{event_id}', response_model=response_schema.OrganizationEvent)
async def update_event(event_id:str, event: request_schema.Event, file:UploadFile=File(...), access_token:str=Form(...)):
    org_id = validate_token_and_id(access_token)
    file_path = None
    if file:
        file_path = GCStorage().upload_file(file)

    return EventService.update_event(event_id, event, file_path, org_id)

@org_event_router.delete('/delete')
async def delete_event(event_id: str, access_token: str):
    org_id = validate_token_and_id(access_token)
    return EventService.delete_event(event_id, org_id)

@org_event_router.put('/submit', response_model=response_schema.OrganizationEvent)
async def submit_event(event_id: str, access_token: str):
    org_id = validate_token_and_id(access_token)
    return EventService.submit_event(event_id, org_id)

@org_event_router.put('/cancel', response_model=response_schema.OrganizationEvent)
async def cancel_event(event_id: str, access_token: str):
    org_id = validate_token_and_id(access_token)
    return EventService.cancel_event(event_id, org_id)