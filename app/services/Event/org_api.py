from typing import Annotated
from fastapi import APIRouter, File, Form, Header, UploadFile
from fastapi.responses import JSONResponse
from . import org_service as EventService, request_schema, response_schema
from app.services.gcs import GCStorage
from app.utils.authentication import validate_token_and_id

org_event_router = APIRouter(prefix="/events/org", tags=['Event Organization'])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/gif"}

@org_event_router.get('/all', response_model=response_schema.OrganizationEventList)
async def get_events(access_token: Annotated[str, Header()]):
    org_id = validate_token_and_id(access_token)
    return EventService.get_all(org_id)

@org_event_router.get('/{event_id}', response_model=response_schema.OrganizationEvent)
async def get_event_by_id(event_id: str, access_token: Annotated[str, Header()]):
    org_id = validate_token_and_id(access_token)
    return EventService.get_event_by_id(event_id, org_id)

@org_event_router.post('/new', response_model=response_schema.OrganizationEvent)
async def post_event(access_token: Annotated[str, Header()], file:UploadFile = File(None), event:request_schema.Event=Form(...)):
    org_id = validate_token_and_id(access_token)
    file_path = "https://storage.cloud.google.com/kumsia-storage/placeholder/event.jpg"
    if file:
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            return JSONResponse({"message": "Invalid file type. Only JPEG, JPG, PNG, and GIF files are allowed."}, status_code=400)
    
        file_path = GCStorage().upload_file(file)

    return EventService.post_event(event, file_path, org_id)

@org_event_router.put('/update/{event_id}', response_model=response_schema.OrganizationEvent)
async def update_event(access_token: Annotated[str, Header()], event_id:str, event: request_schema.Event, file:UploadFile = File(None)):
    org_id = validate_token_and_id(access_token)
    file_path = None
    if file:
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            return JSONResponse({"message": "Invalid file type. Only JPEG, JPG, PNG, and GIF files are allowed."}, status_code=400)
    
        file_path = GCStorage().upload_file(file)

    return EventService.update_event(event_id, event, file_path, org_id)

@org_event_router.delete('/delete')
async def delete_event(event_id: str, access_token: Annotated[str, Header()]):
    org_id = validate_token_and_id(access_token)
    return EventService.delete_event(event_id, org_id)

@org_event_router.put('/submit', response_model=response_schema.OrganizationEvent)
async def submit_event(event_id: str, access_token: Annotated[str, Header()]):
    org_id = validate_token_and_id(access_token)
    return EventService.submit_event(event_id, org_id)

@org_event_router.put('/cancel', response_model=response_schema.OrganizationEvent)
async def cancel_event(event_id: str, access_token: Annotated[str, Header()]):
    org_id = validate_token_and_id(access_token)
    return EventService.cancel_event(event_id, org_id)