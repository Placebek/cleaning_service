import asyncio

from fastapi import HTTPException
from jose import JWTError
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.commands.auth_admin_crud import get_requests
from app.api.auth.commands.context import create_access_token, validate_access_token_by_tg_id
from app.api.auth.shemas.create import RequestCreate, UserCreate
from app.api.auth.shemas.response import StatusResponse, TokenResponse, CityResponse
from model.model import *
from websocket import manager

flag = asyncio.Event()

async def validate_user_from_token_by_tg_id(access_token: str, db: AsyncSession) -> User:
    try:
        tg_id = await validate_access_token_by_tg_id(access_token=access_token)

        stmt = await db.execute(
            select(User)
            .filter(User.tg_id == int(tg_id))
        )
        user = stmt.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

async def user_register(user: UserCreate, db: AsyncSession):
    stmt = await db.execute(
        select(User)
        .filter(
            User.tg_id==user.tg_id
        )
    )
    existing_user = stmt.scalar_one_or_none()

    if not existing_user:
        new_user = User(
            tg_username=user.tg_username,
            tg_id=user.tg_id
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

    access_token, expire_time = create_access_token(data={"sub": str(existing_user.tg_id)})
    return TokenResponse(
        access_token=access_token,
        access_token_expire_time=expire_time
    )


async def post_volume(data: VolumeWork, access_token: str, db: AsyncSession):
    
    db_cleaning_type = await db.execute(
        insert(CleaningType)
        .values(
            cleaning_type=data.cleaning_type
        )
        .returning(CleaningType.id)
    ) 
    cleaning_type_id = db_cleaning_type.fetchone()[0]


    db_premises_type = await db.execute(
        insert(PremisesType)
        .values(
            premises_type=data.cleaning_type
        )
        .returning(PremisesType.id)
    ) 
    premises_type_id = db_premises_type.fetchone()[0]

    db_volume_work = await db.execute(
        insert(VolumeWork)
        .values(
            worker_count=1,
            cleaning_type_id=cleaning_type_id,
            premises_type_id=premises_type_id,
        )
        .returning(VolumeWork.id)
    )
    volume_work_id = db_volume_work.fetchone()[0]

    return volume_work_id


async def post_requests(data: RequestCreate, access_token: str, db: AsyncSession):
    user = await validate_user_from_token_by_tg_id(access_token=access_token, db=db)
    db_city = await db.execute(
        select(City.id)
        .filter(
            City.city_name==data.city_name
        )
    )
    city_id = db_city.scalars().first()

    db_street = await db.execute(
        select(Street.id)
        .filter(
            Street.street_name==data.street_name
        )
    )
    street_id = db_street.scalars().first()


    if street_id == None:
        db_street = await db.execute(
        insert(Street)
        .values(
            street_name=data.street_name
        )
        .returning(Street.id)
        )
        street_id = db_street.fetchone()[0]
        

    await db.commit()
    print(data, city_id, street_id)
    db_address = await db.execute(
        insert(Address)
        .values(
            city_name_id=city_id,
            street_name_id=street_id,
            house_number=data.house_number,
            apartment_number=data.apartment_number,
        )
        .returning(Address.id)
    )
    await db.commit()
    address_id = db_address.fetchone()[0]


    await db.execute(
        update(User)
        .values(
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone_number,
            address_id=address_id
        )
        .where(
            User.id==user.id,
        )
    ) 

    await post_volume(data=data, access_token=access_token, db=db)

    db_request = await db.execute(
        insert(Request)
        .values(
            user_id=user.id,
            date=data.date,
            address_id=address_id,
            volume_work_id=await post_volume(data=data, access_token=access_token, db=db)
            
        )
        .returning(Request.id)
    )

    await db.commit()
    flag.set()

    request_id = db_request.fetchone()[0]
    print('доходит до весокета работает')
    updated_request = await get_requests(access_token=access_token, db=db )
    await manager.broadcast(updated_request)
    print('доходит до весокета работает2')


    return StatusResponse(status_code=201, status_msg=f"Reques saved successfully your request id = {request_id}")


async def get_cities(access_token: str, db: AsyncSession):
    await validate_user_from_token_by_tg_id(access_token=access_token, db=db)

    stmt = await db.execute(
        select(City.city_name)
    )
    cities = stmt.all()

    return [CityResponse.from_orm(city) for city in cities]


async def get_cities_by_name(city_name: str, access_token: str, db: AsyncSession):
    await validate_user_from_token_by_tg_id(access_token=access_token, db=db)

    city = await db.execute(
        select(City.city_name)
        .filter(
            City.city_name == city_name
        )
    )
    city_name = city.scalar_one_or_none()


    return CityResponse(city_name=city_name)
