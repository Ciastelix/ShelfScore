from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class ReviewInCreate(BaseModel):
    user_id: UUID
    book_id: UUID
    rating: int
    review: str


class ReviewInUpdate(BaseModel):
    user_id: Optional[UUID]
    book_id: Optional[UUID]
    rating: Optional[int]
    review: Optional[str]
    is_active: Optional[bool]

    class Config:
        orm_mode = True


class ReviewInDB(BaseModel):
    id: UUID
    user_id: UUID
    book_id: UUID
    rating: int
    review: str
    is_active: bool

    class Config:
        orm_mode = True
