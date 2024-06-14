from fastapi import APIRouter
from . import service, response_schema as MasterDataService

master_data_router = APIRouter(prefix="/masterdata", tags=['Master Data'])

@master_data_router.get('/hobby', response_model=MasterDataService.HobbyList)
async def get_master_hobby():
    return service.get_master_hobby()

@master_data_router.get('/city', response_model=MasterDataService.CityList)
async def get_master_city():
    return service.get_master_city()