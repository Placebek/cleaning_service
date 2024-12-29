from json import dumps
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
from jose import JWTError
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects import postgresql


from app.api.auth.shemas.create import AdminBase, RequestBase, WorkerCreate
from app.api.auth.shemas.response import TokenResponse, UserResponse, RequestResponse, WorkersResponse, StatusResponse, OrdersResponse
from app.api.auth.commands.context import validate_access_token, verify_password, create_access_token, validate_access_token_by_tg_id
from model.model import *
from websocket import manager




async def validate_admin_from_token(access_token: str, db: AsyncSession) -> User:
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


        if not db_admin or  verify_password(user.password, db[0].hashed_password):
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
    await validate_admin_from_token(access_token=access_token, db=db)

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




async def  get_requests(access_token: str, db: AsyncSession):
    await validate_access_token_by_tg_id(access_token=access_token)
    print('get_req работает')

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
            City.city_name,
            Street.street_name,
            Address.house_number,
            Address.apartment_number,
            Order.request_id ,
            )
        .join(User, Request.user_id==User.id)
        .join(VolumeWork, Request.volume_work_id == VolumeWork.id)
        .join(PremisesType, VolumeWork.premises_type_id==PremisesType.id)
        .join(CleaningType, VolumeWork.cleaning_type_id==CleaningType.id)
        .join(Address, User.address_id==Address.id)
        .join(City, City.id==Address.city_name_id)
        .join(Street, Street.id==Address.street_name_id)
        .outerjoin(Order, Order.request_id==Request.id)
        .filter(Order.request_id.is_(None))
    )

    requests = stmt.all()

    return [RequestResponse.from_orm(request) for request in requests]


async def get_workers(access_token: str, db: AsyncSession):
    await validate_admin_from_token(access_token=access_token, db=db)

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
    await validate_admin_from_token(access_token=access_token, db=db)

    stmt = await db.execute(
        select(
            Order.id,
            Status.status_name,
            User.first_name,
            User.last_name,
            CleaningType.cleaning_type,
            PremisesType.premises_type,
            Request.date,
            Worker.photo
        )
        .outerjoin(Status, Status.id==Order.status_id)
        .join(Request, Request.id==Order.request_id)
        .join(VolumeWork, VolumeWork.id==Request.volume_work_id)
        .join(CleaningType, CleaningType.id==VolumeWork.cleaning_type_id)
        .join(PremisesType, PremisesType.id==VolumeWork.premises_type_id)
        .join(Worker, Worker.id==Order.worker_id)
        .join(User, User.id==Request.user_id)
    )

    orders = stmt.all()
    return [OrdersResponse.from_orm(order) for order in orders]


async def upgrade_request(request_data: RequestBase, access_token: str, db: AsyncSession):
    admin = await validate_admin_from_token(access_token=access_token, db=db)

    stmt = await db.execute(
        select(Request)
        .filter(Request.id==request_data.request_id)
    )

    request = stmt.scalars().first()

    if not request:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_order = Order(
        worker_id=request_data.worker_id,
        admin_id=admin.id,
        request_id=request.id,
        # status_id=status_id,
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(request)
    updated_request = await get_requests(access_token=access_token, db=db)
    await manager.broadcast(updated_request)
    
    return StatusResponse(status_code=201, status_msg="Upgrade order")



async def delete_orders(order_id: int, access_token: str, db: AsyncSession):
    await validate_admin_from_token(access_token=access_token, db=db)

    stmt = await db.execute(
        select(Order)
        .filter(Order.id == order_id)
        )
    order = stmt.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="Music not found")

    await db.delete(order)
    await db.commit()

    remain_orders = await get_orders(access_token=access_token, db=db)
    new_orders = []
    for item in remain_orders:
        new_date = dict(item)
        new_date['date'] = str(dict(item)['date'])
        new_orders.append(new_date)

    await manager.broadcast(new_orders)

    return StatusResponse(status_code=201, status_msg=f"Delete order where id == {order_id}")


async def delete_request(request_id: int, access_token: str, db: AsyncSession):
    await validate_admin_from_token(access_token=access_token, db=db)

    stmt = await db.execute(
        select(Request)
        .filter(Request.id == request_id)
        )
    order = stmt.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="Request not found")

    await db.delete(order)
    await db.commit()

    updated_request = await get_requests(access_token=access_token, db=db)
    await manager.broadcast(updated_request)
    
    return StatusResponse(status_code=201, status_msg=f"Delete request where id == {request_id}")


async def upgrade_workers(worker_data: WorkerCreate, access_token: str, db: AsyncSession):
    await validate_admin_from_token(access_token=access_token, db=db)
    stmt = await db.execute(
        select(User)
        .filter(User.id==worker_data.worker_id)
    )
    worker = stmt.scalar_one_or_none()

    if not worker:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.execute(
        update(Worker)
        .values(
            photo=worker_data.photo,
            experience=worker_data.experience,
            is_active=worker_data.is_active,
            user_id=worker.id,
            first_name=worker_data.first_name,
            last_name=worker_data.last_name,
            phone_number=worker_data.phone_number,
        )
        .where(
            Worker.id == worker_data.worker_id,
        )
    )

    await db.commit()

    return StatusResponse(status_code=201, status_msg="Upgrade worker")
