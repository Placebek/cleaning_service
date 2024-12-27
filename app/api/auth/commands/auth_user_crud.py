from fastapi import HTTPException
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.commands.context import hash_password, validate_access_token
from app.api.auth.shemas.create import UserBase, UserCreate
from app.api.auth.shemas.response import StatusResponse
from model.model import User


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
    

async def user_register(user: UserCreate, db: AsyncSession) -> StatusResponse:
    stmt = await db.execute(
        select(User)
        .filter(
            User.tg_id==user.tg_id
        )
    )
    existing_user = stmt.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        tg_username=user.tg_username,
        tg_id=user.tg_id,
        city_name_id=user.city_name_id,
        street_name_id=user.street_name_id,
        house_number=user.house_number,
        apartment_number=user.apartment_number,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return StatusResponse(status_code=201, status_msg="User registered successfully")


# async def user_login(user: UserBase, db: AsyncSession):
    
