from typing import Annotated
from fastapi import APIRouter, Header

from app.utils.authentication import validate_token_and_id
from . import request_schema, comment_service as CommentService

comment_router = APIRouter(prefix="/comment", tags=['Comment'])

@comment_router.get('/all')
async def get_all_by_event(event_id: str):
    return CommentService.get_all_by_event(event_id)

@comment_router.post('/create')
async def comment_event(comment: request_schema.Comment, access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return CommentService.post_comment(comment, user_id)

@comment_router.delete('/delete')
async def uncomment_event(comment_id: str, access_token: Annotated[str, Header()]):
    user_id = validate_token_and_id(access_token)
    return CommentService.delete_comment(comment_id, user_id)