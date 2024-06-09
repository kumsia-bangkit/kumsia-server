from fastapi import APIRouter
from . import like_service as LikeService

like_router = APIRouter(prefix="/like", tags=['Like'])

@like_router.get('/is_liked')
async def get_is_liked(event_id: str):
    return LikeService.is_liked(event_id)

@like_router.post('/create')
async def like_event(event_id: str):
    return LikeService.post_like(event_id)

@like_router.delete('/delete')
async def unlike_event(event_id: str):
    return LikeService.delete_like(event_id)