from sqlalchemy import Column, String, Boolean
from sqlalchemy.sql.schema import ForeignKey

from db import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum


class RoleEnum(Enum):
    ADMIN = "admin"
    CLIENT = "client"
    PROJECT_MANAGER = "project_manager"
    WORKER = "worker"


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
