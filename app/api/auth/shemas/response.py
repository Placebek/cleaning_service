from datetime import datetime
from json import dumps
from typing import Annotated, Optional
from pydantic import BaseModel

class StatusResponse(BaseModel):
    status_code: int
    status_msg: str
    
class TokenResponse(BaseModel):
    access_token: str
    access_token_expire_time: datetime
    access_token_type: str = 'Bearer'

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    tg_username: str
    tg_id: int
    address_id: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes=True

class RequestResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    volume_work_id: Optional[int] = None
    first_name: str
    last_name: str
    phone_number: str
    worker_count: int
    premises_type: str
    cleaning_type: str
    city_name: str
    street_name: str
    house_number: int
    apartment_number: int
    request_id: Optional[int] = None

    class Config:
        from_attributes=True


class OrdersResponse(BaseModel):
    id: int
    status_name: Optional[int] = None
    first_name: str
    last_name: str
    cleaning_type: str
    premises_type: str
    date: datetime
    photo: str
    class Config:
        from_attributes=True


class WorkersResponse(BaseModel):
    id: int
    photo: str
    experience: Optional[int] = None
    is_active: bool
    user_id: int
    first_name: str
    last_name: str
    phone_number: str

    class Config:
        from_attributes=True

class CityResponse(BaseModel):
    city_name: str
    
    class Config:
        from_attributes=True