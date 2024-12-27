from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from app.api.auth.shemas.create import AdminBase
from app.api.auth.shemas.response import TokenResponse, UserResponse, RequestResponse, WorkersResponse, OrdersResponse
from app.api.auth.commands.auth_admin_crud import admin_login, get_orders, get_requests, get_users, get_workers
from app.api.auth.commands.context import get_access_token

router = APIRouter()

@router.post(
    '/login',
    summary='access_token алу',
    response_model=TokenResponse
)
async def login(user: AdminBase, db: AsyncSession = Depends(get_db)):
    return await admin_login(user=user, db=db)


@router.get(
    '/users',
    summary="get user profile data",
    response_model=List[UserResponse]
)
async def users(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await get_users(access_token=access_token, db=db)


@router.get(
    '/requests',
    summary="",
    response_model=List[RequestResponse]
)
async def requests(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await get_requests(access_token=access_token, db=db)


@router.get(
    '/workers',
    summary="",
    response_model=List[WorkersResponse]
)
async def workers(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await get_workers(access_token=access_token, db=db)


@router.get(
    '/orders',
    summary="",
    response_model=List[OrdersResponse]
)
async def orders(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await get_orders(access_token=access_token, db=db)
