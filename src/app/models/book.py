from __future__ import annotations
import os
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from ..db import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

IMAGE_URL = os.getenv("IMAGE_URL", "shelf/public/images")


class Book(Base):
    __tablename__ = "books"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    author_id = Column(
        UUID(as_uuid=True), ForeignKey("authors.id"), nullable=False
    )
    genre = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    image = Column(String, nullable=True, default=f"{IMAGE_URL}/books/default.png")
    is_active = Column(Boolean, default=True)

    author = relationship("Author", back_populates="books")
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")
