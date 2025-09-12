from typing import Optional
from pydantic import BaseModel
from pydantic import ConfigDict
from uuid import UUID


class UserInCreate(BaseModel):
    username: str
    email: str
    password: str


class UserInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
    picture: Optional[str] = None
    is_active: Optional[bool] = None


class UserUpdatePassword(BaseModel):
    password: str
    new_password: str


class UserInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    username: str
    email: str
    description: Optional[str] = None
    picture: Optional[str] = None
    is_active: bool = True
