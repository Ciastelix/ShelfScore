from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class UserInCreate(BaseModel):
    username: str
    email: str
    password: str
    name: str
    surname: str


class UserInDB(BaseModel):
    username: str
    email: str


class WorkerInResponseUser(BaseModel):
    id: UUID
    name: str
    surname: str
    username: str
    email: str
    is_active: bool


class UserInResponse(BaseModel):
    id: UUID
    name: str
    surname: str
    username: str
    email: str
    is_active: bool


class UserInUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
