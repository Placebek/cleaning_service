import hashlib
from fastapi import HTTPException
from jose import JWTError
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.shemas.create import AdminBase
from app.api.auth.shemas.response import TokenResponse, UserResponse, RequestResponse, WorkersResponse, StatusResponse, OrdersResponse
from app.api.auth.commands.context import hash_password, validate_access_token, verify_password, create_access_token
from model.model import *


async def validate_user_from_token(access_token: str, db: AsyncSession) -> User:
    try:
        username = await validate_access_token(access_token=access_token)

        stmt = await db.execute(
            select(User)
            .filter(User.tg_username == username)
        )
        user = stmt.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

async def admin_login(user: AdminBase, db: AsyncSession) -> TokenResponse:
    try:
        db_admin = await db.execute(
            select(Admin, User.tg_username)
            .join(User)
            .filter(User.tg_id==user.tg_id)
        )
        db = db_admin.one_or_none()
        # print("ADMIN: ", dir(db[0]), db[1])
    
        if not db_admin or not verify_password(user.password, db[0].hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        access_token, expire_time = create_access_token(data={"sub": db[1]})

        return TokenResponse(
            access_token=access_token,
            access_token_expire_time=expire_time
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during login: {str(e)}"
        )


async def get_users(access_token: str, db: AsyncSession):
    await validate_user_from_token(access_token=access_token, db=db)

    stmt = await db.execute(
        select(
            User.id,
            User.first_name,
            User.last_name,
            User.phone_number,
            User.tg_username,
            User.tg_id,
            User.address_id,
            User.created_at,
        )
    )
    users = stmt.all()
    return [UserResponse.from_orm(user) for user in users]


async def get_requests(access_token: str, db: AsyncSession):
    await validate_user_from_token(access_token=access_token, db=db)

    stmt = await db.execute(
        select(
            Request.id,
            Request.user_id,
            Request.volume_work_id,
            User.first_name,
            User.last_name,
            User.phone_number,
            VolumeWork.worker_count,
            PremisesType.premises_type,
            CleaningType.cleaning_type,
            )
        .join(User, Request.user_id==User.id)
        .join(VolumeWork, Request.volume_work_id == VolumeWork.id)
        .join(PremisesType, VolumeWork.premises_type_id==PremisesType.id)
        .join(CleaningType, VolumeWork.cleaning_type_id==CleaningType.id)
    )

    requests = stmt.all()

    return [RequestResponse.from_orm(request) for request in requests]


async def get_workers(access_token: str, db: AsyncSession):
    await validate_user_from_token(access_token=access_token, db=db)

    stmt = await db.execute(
        select(
            Worker.id,
            Worker.photo,
            Worker.experience,
            Worker.is_active,
            Worker.user_id,
            User.first_name,
            User.last_name,
            User.phone_number,
        )
        .join(User, Worker.user_id==User.id)
        .filter(Worker.is_active==True)
    )

    workers = stmt.all()

    return [WorkersResponse.from_orm(worker) for worker in workers]


async def get_orders(access_token: str, db: AsyncSession):
    await validate_user_from_token(access_token=access_token, db=db)

    stmt = await db.execute(
        select(
            Order.worker_id,
            Order.admin_id,
            Order.request_id,
            Order.status_id,
        )
    )

    orders = stmt.all()

    return [OrdersResponse.from_orm(order) for order in orders]


async def upgrade_orders(worker_id: int, order_id: int, access_token: str, db: AsyncSession):
    admin = await validate_user_from_token(access_token=access_token, db=db)
    print("ADMIN: ", admin)
    stmt = await db.execute(
        select(Order)
        .filter(Order.id==order_id)
    )

    order = stmt.scalars().first()
    print(order)

    if not order:
        raise HTTPException(status_code=404, detail="User not found")
        
    upgrade_order = await db.execute(
        update(Order)
        .values(
            worker_id=worker_id,
            admin_id=admin.id,
        )
        .where(
            Order.id == order_id,
        )
    )

    await db.commit()

    return StatusResponse(status_code=201, status_msg="Upgrade order")


async def delete_orders(order_id: int, access_token: str, db: AsyncSession):
    await validate_user_from_token(access_token=access_token, db=db)

    stmt = await db.execute(
        select(Order)
        .filter(Order.id == order_id)
        )
    order = stmt.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="Music not found")

    await db.delete(order)
    await db.commit()

    return StatusResponse(status_code=201, status_msg=f"Delete order where id == {order_id}")

async def delete_request(request_id: int, access_token: str, db: AsyncSession):
    await validate_user_from_token(access_token=access_token, db=db)

    stmt = await db.execute(
        select(Request)
        .filter(Request.id == request_id)
        )
    order = stmt.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="Music not found")

    await db.delete(order)
    await db.commit()

    return StatusResponse(status_code=201, status_msg=f"Delete order where id == {request_id}")
    