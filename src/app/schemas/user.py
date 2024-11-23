from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class UserInCreate(BaseModel):
    username: str
    email: str
    password: str


class UserInUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    description: Optional[str]
    picture: Optional[str]
    is_active: Optional[bool]

    class Config:
        from_model = True


class UserUpdatePassword(BaseModel):
    password: str
    new_password: str


class UserInDB(BaseModel):
    id: UUID
    username: str
    email: str
    description: str
    picture: str
    is_active: bool
