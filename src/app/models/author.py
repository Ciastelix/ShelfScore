from __future__ import annotations
from sqlalchemy import Column, String, Boolean
from db import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Author(Base):
    __tablename__ = "authors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    description = Column(String, nullable=True, default="No description")
    is_active = Column(Boolean, default=True)
    year_born = Column(String, nullable=False, default="Unknown")
    photo = Column(String, nullable=True, default="default.png")
    books = relationship("Book", back_populates="author")
