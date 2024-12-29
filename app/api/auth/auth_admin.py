from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from app.api.auth.shemas.create import AdminBase, RequestBase, WorkerCreate
from app.api.auth.shemas.response import TokenResponse, UserResponse, RequestResponse, WorkersResponse, OrdersResponse, StatusResponse
from app.api.auth.commands.auth_admin_crud import admin_login, delete_orders, delete_request, get_orders, get_requests, get_users, get_workers, upgrade_request, upgrade_workers
from app.api.auth.commands.context import get_access_token
from websocket import manager

router = APIRouter()



@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data: {data}")
    except WebSocketDisconnect:
        print(f"Disconnecting: {websocket}")
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")



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


@router.post(
    '/requests',
    summary="",
    response_model=StatusResponse
)
async def request(request_data: RequestBase, access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await upgrade_request(access_token=access_token, db=db, request_data=request_data)


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


@router.put(
    '/workers',
    summary="",
    response_model=StatusResponse
)
async def workers(worker_data: WorkerCreate, access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await upgrade_workers(worker_data=worker_data, access_token=access_token, db=db)
