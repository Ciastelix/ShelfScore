from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class BookInCreate(BaseModel):
    title: str
    author_id: UUID
    genre: str
    year: int
    description: str
    image: str


class BookInUpdate(BaseModel):
    title: Optional[str]
    author_id: Optional[UUID]
    genre: Optional[str]
    year: Optional[int]
    description: Optional[str]
    image: Optional[str]
    is_active: Optional[bool]

    class Config:
        from_model = True


class BookInDB(BaseModel):
    id: UUID
    title: str
    author_id: UUID
    genre: str
    year: int
    description: str
    image: str
    is_active: bool
