from __future__ import annotations
from sqlalchemy import Column, String, Boolean
from db import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    description = Column(String, nullable=True, default="")
    picture = Column(String, nullable=True, default="default.png")
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    user_reviews = relationship("Review", back_populates="user")
