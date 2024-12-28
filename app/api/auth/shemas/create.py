from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AdminBase(BaseModel):
    tg_id: int
    password: str

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    tg_username: str
    tg_id: int
    city_name_id: str
    street_name_id: str
    house_number: int
    apartment_number: int

class UserBase(BaseModel):
    tg_username: str
    tg_id: int


class OrderCreate(BaseModel):
    order_id: int
    worker_id: int
    status_id: Optional[int] = None