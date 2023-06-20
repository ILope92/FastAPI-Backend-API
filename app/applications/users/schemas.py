from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseProperties(BaseModel):
    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={"id", "is_superuser", "is_active", "password"},
        )


class BaseUser(BaseProperties):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    created_at: Optional[datetime]


class BaseUserCreate(BaseProperties):
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    password: str

    def to_dict_user(self):
        del self.password
        return self.create_update_dict()


class BaseUserUpdate(BaseProperties):
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr]
    username: Optional[str]

    def to_dict_user(self):
        del self.password
        return self.create_update_dict()


class BaseUserOut(BaseUser):
    id: int

    class Config:
        orm_mode = True


class JWTTokenPayload(BaseModel):
    user_id: int = None
