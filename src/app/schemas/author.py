from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class AuthorInCreate(BaseModel):
    name: str
    surname: str
    description: str
    year_born: str


class AuthorInUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    description: Optional[str]
    is_active: Optional[bool]
    year_born: Optional[str]

    class Config:
        from_model = True


class AuthorInDB(BaseModel):
    id: UUID
    name: str
    surname: str
    description: str
    is_active: bool
    year_born: str
    photo: Optional[str]
