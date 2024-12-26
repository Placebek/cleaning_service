from datetime import datetime
from pydantic import BaseModel

class StatusResponse(BaseModel):
    status_code: int
    status_msg: str
    
class TokenResponse(BaseModel):
    access_token: str
    access_token_expire_time: datetime
    access_token_type: str = 'Bearer'

class UserResponse(BaseModel):
    pass