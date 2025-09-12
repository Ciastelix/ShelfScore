from typing import Optional
from pydantic import BaseModel
from pydantic import ConfigDict
from uuid import UUID


class BookInCreate(BaseModel):
    title: str
    author_id: UUID
    genre: str
    year: int
    description: str


class BookInUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[UUID] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: Optional[bool] = None


class BookInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    author_id: UUID
    genre: str
    year: int
    description: str
    image: Optional[str] = None
    is_active: bool = True
