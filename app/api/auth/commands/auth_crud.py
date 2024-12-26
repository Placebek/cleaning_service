import hashlib
from fastapi import HTTPException
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.shemas.create import UserBase
from app.api.auth.shemas.response import StatusResponse, TokenResponse
from app.api.auth.commands.context import hash_password, validate_access_token, verify_password, create_access_token
from model.model import *


async def validate_user_from_token(access_token: str, db: AsyncSession) -> User:
    try:
        username = await validate_access_token(access_token=access_token)

        stmt = await db.execute(
            select(User)
            .filter(User.username == username)
        )
        user = stmt.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

async def admin_register(user: UserBase, db: AsyncSession) -> StatusResponse:
    stmt = await db.execute(
        select(User)
        .filter(User.username == user.username)
    )
    existing_user =  stmt.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = hash_password(user.password)

    new_user = AdminUser(
        hashed_password=hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return StatusResponse(status_code=201, status_msg="User registered successfully")


async def admin_login(user: UserBase, db: AsyncSession) -> TokenResponse:
    try:
        stmt = await db.execute(
            select(User)
            .filter(User.username == user.username)
        )
        db_user = stmt.scalar_one_or_none()

        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        access_token, expire_time = create_access_token(data={"sub": db_user.username})

        return TokenResponse(
            access_token=access_token,
            access_token_expire_time=expire_time
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during login: {str(e)}"
        )


async def user_profile(access_token: str, db: AsyncSession):
    user = validate_user_from_token(access_token=access_token, db=db)

    result  = await db.execute(
        select(User)
        .filter(User.id==user.id)
    )
    user_data = result.one_or_none()

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_data
