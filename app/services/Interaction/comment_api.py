from fastapi import APIRouter
from . import request_schema, comment_service as CommentService

comment_router = APIRouter(prefix="/comment", tags=['Comment'])

@comment_router.get('/all')
async def get_all_by_event(event_id: str):
    return CommentService.get_all_by_event(event_id)

@comment_router.post('/create')
async def comment_event(comment: request_schema.Comment):
    return CommentService.post_comment(comment)

@comment_router.delete('/delete')
async def uncomment_event(comment_id: str):
    return CommentService.delete_comment(comment_id)