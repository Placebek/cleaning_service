from datetime import date
from typing import Optional
from pydantic import BaseModel


class AdminBase(BaseModel):
    tg_id: int
    password: str

class UserCreate(BaseModel):
    tg_username: str
    tg_id: int

class RequestCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

    city_name: Optional[str] = None
    street_name: Optional[str] = None
    house_number: Optional[int] = None
    apartment_number: Optional[int] = None
    date: date

class OrderCreate(BaseModel):
    order_id: int
    worker_id: int
    status_id: Optional[int] = None
    
class WorkerCreate(BaseModel):
    worker_id: Optional[int]
    photo: Optional[str]
    experience: Optional[int]
    is_active: Optional[bool]
    # user_id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]

    class Config:
        from_attributes=True

class RequestBase(BaseModel):
    request_id: int
    worker_id: int
