from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from db import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("authors.id"), nullable=False)
    genre = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    author = relationship("Author", back_populates="books")
    reviews = relationship("Review", back_populates="book")
