from contextlib import AbstractContextManager
from typing import Callable, Any
from sqlalchemy.orm import Session
from schemas.user import UserInCreate, UserInUpdate, UserUpdatePassword
from models.user import User
from models.review import Review
from utils.security import get_password_hash, verify_password
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
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        with self.session_factory() as session:
            return session.query(User).filter_by(id=user_id).first()

    def update(self, user_id: UUID, user_new: UserInUpdate) -> User:
        if isinstance(user_id, str):
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

    def add_image(self, user_id: UUID, image_path: str) -> User:
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        with self.session_factory() as session:
            user = session.query(User).filter_by(id=user_id).first()
            user.picture = image_path
            session.commit()
            session.refresh(user)
            return user

    def delete(self, user_id: UUID) -> None:
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        with self.session_factory() as session:
            user = session.query(User).filter_by(id=user_id).first()
            session.delete(user)
            session.commit()

    def get_me(self, user: UserInCreate) -> User:
        with self.session_factory() as session:
            usr = session.query(User).filter_by(email=user.email).first()
            if verify_password(user.password, usr.password):
                return usr

    def change_password(
        self, updated_password: UserUpdatePassword, current_user: Any
    ) -> User:
        user_id = current_user.id
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        with self.session_factory() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if verify_password(updated_password.password, user.password):
                user.password = get_password_hash(updated_password.new_password)
                session.commit()
                session.refresh(user)
                return user
            else:
                raise ValueError("Current password is incorrect")

    def get_books_read_by_user_with_author(self, user_id: UUID):
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        with self.session_factory() as session:
            reviews = session.query(Review).filter(Review.user_id == user_id).all()
            books = []
            for review in reviews:
                book = review.book
                author = book.author
                books.append(
                    {
                        "id": book.id,
                        "title": book.title,
                        "genre": book.genre,
                        "year": book.year,
                        "description": book.description,
                        "image": book.image,
                        "is_active": book.is_active,
                        "author_name": author.name,
                        "author_surname": author.surname,
                    }
                )
            return books
