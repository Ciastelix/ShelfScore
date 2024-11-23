from __future__ import annotations
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from db import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Review(Base):
    __tablename__ = "reviews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=True)
    rating = Column(Integer, nullable=False)
    review = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    user = relationship("User", back_populates="user_reviews")
    book = relationship("Book", back_populates="reviews")
