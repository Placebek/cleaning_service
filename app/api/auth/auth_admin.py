from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from app.api.auth.shemas.create import UserBase
from app.api.auth.shemas.response import StatusResponse, TokenResponse, UserResponse
from app.api.auth.commands.auth_crud import admin_register, admin_login, user_profile
from app.api.auth.commands.context import get_access_token

router = APIRouter()

@router.post(
    '/register',
    summary="Тіркелу",
    response_model=StatusResponse
)
async def admin_register(user: UserBase, db: AsyncSession = Depends(get_db)):
    return await admin_register(user=user, db=db)


@router.post(
    '/login',
    summary='access_token алу',
    response_model=TokenResponse
)
async def login(user: UserBase, db: AsyncSession = Depends(get_db)):
    return await admin_login(user=user, db=db)


@router.get(
    '/profile',
    summary="get user profile data",
    response_model=UserResponse
)
async def profile(access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await user_profile(access_token=access_token, db=db)


@router.put(
    '/profile',
    summary="Change profile",
    response_model=StatusResponse
)
async def profile_user(update_data: UserCreate, access_token: str = Depends(get_access_token), db: AsyncSession = Depends(get_db)):
    return await bll_update_user_profile(update_data=update_data, access_token=access_token, db=db)
