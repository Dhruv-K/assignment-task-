from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True


class UserMe(UserBase):
    created_at: datetime
