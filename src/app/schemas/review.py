from typing import Optional
from pydantic import BaseModel
from pydantic import ConfigDict
from uuid import UUID


class ReviewInCreate(BaseModel):
    user_id: UUID
    book_id: UUID
    rating: int
    review: str


class ReviewInUpdate(BaseModel):
    user_id: Optional[UUID] = None
    book_id: Optional[UUID] = None
    rating: Optional[int] = None
    review: Optional[str] = None
    is_active: Optional[bool] = None


class ReviewInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    book_id: UUID
    rating: int
    review: Optional[str] = None
    is_active: bool = True
