from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from app.api.auth.shemas.create import AdminBase
from app.api.auth.shemas.response import TokenResponse, UserResponse, RequestResponse, WorkersResponse, OrdersResponse, StatusResponse
from app.api.auth.commands.auth_admin_crud import admin_login, delete_orders, delete_request, get_orders, get_requests, get_users, get_workers, upgrade_orders
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


@router.put(
    '/orders/{order_id}/{worker_id}',
    summary="",
    response_model=StatusResponse
)
async def orders(order_id: int, worker_id: int, access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await upgrade_orders(access_token=access_token, db=db, order_id=order_id, worker_id=worker_id)


@router.delete(
    '/orders/{order_id}',
    summary="",
    response_model=StatusResponse
)
async def orders(order_id: int, access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await delete_orders(access_token=access_token, db=db, order_id=order_id)


@router.delete(
    '/request/{request_id}',
    summary="",
    response_model=StatusResponse
)
async def orders(request_id: int, access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await delete_request(access_token=access_token, db=db, request_id=request_id)
