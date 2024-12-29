from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.commands.context import get_access_token
from app.api.auth.shemas.create import RequestCreate, UserCreate
from app.api.auth.shemas.response import StatusResponse, CityResponse, TokenResponse
from app.api.auth.commands.auth_user_crud import get_cities, get_cities_by_name, post_requests, user_register # post_requests, user_login
from database.db import get_db

router = APIRouter()

@router.post(
    '/register',
    summary="",
    response_model=TokenResponse
)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_register(user=user, db=db)

@router.post(
    '/request',
    summary="",
    response_model=StatusResponse
)
async def request(data: RequestCreate,access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await post_requests(data=data, access_token=access_token, db=db)


@router.get(
    '/cities/{city_name}',
    summary="",
    response_model=CityResponse
)
async def cities_by_name(city_name: str, access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await get_cities_by_name(city_name=city_name, access_token=access_token, db=db)


@router.get(
    '/cities',
    summary="",
    response_model=List[CityResponse]
)
async def cities(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await get_cities(access_token=access_token, db=db)
