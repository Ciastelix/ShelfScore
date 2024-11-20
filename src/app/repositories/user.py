from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from schemas.user import UserInCreate, UserInUpdate
from models.user import User

from utils.password import get_password_hash
from uuid import UUID


class UserRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def add(self, user: UserInCreate) -> User:
        with self.session_factory() as session:
            user.password = get_password_hash(user.password)
            user = User(**user.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)
        return user

    def get_all(self) -> list[User]:
        with self.session_factory() as session:
            return session.query(User).all()

    def get_by_id(self, user_id: UUID) -> User:
        if type(user_id) == str:
            user_id = UUID(user_id)
        with self.session_factory() as session:
            return session.query(User).filter_by(id=user_id).first()

    def update(self, user_id: UUID, user_new: UserInUpdate) -> User:
        if type(user_id) == str:
            user_id = UUID(user_id)
        with self.session_factory() as session:
            if user_new.password:
                user_new.password = get_password_hash(user_new.password)
            user = session.query(User).filter_by(id=user_id).first()
            for key, value in user_new.model_dump().items():
                setattr(user, key, value)
            session.commit()
            session.refresh(user)
            return user

    def delete(self, user_id: UUID) -> None:
        if type(user_id) == str:
            user_id = UUID(user_id)
        with self.session_factory() as session:
            user = session.query(User).filter_by(id=user_id).first()
            session.delete(user)
            session.commit()

    def get_me(self, user: UserInCreate) -> User:
        with self.session_factory() as session:
            usr = session.query(User).filter_by(email=user.email).first()
            if usr.password == get_password_hash(user.password):
                return usr
