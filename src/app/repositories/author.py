from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from schemas.author import AuthorInCreate, AuthorInDB, AuthorInUpdate
from models.author import Author
from uuid import UUID


class AuthorRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def add(self, author: AuthorInCreate) -> AuthorInDB:
        with self.session_factory() as session:
            author = Author(**author.model_dump())
            session.add(author)
            session.commit()
            session.refresh(author)
        return author

    def get_all(self) -> list[AuthorInDB]:
        with self.session_factory() as session:
            return session.query(AuthorInDB).all()

    def get_by_id(self, author_id: UUID) -> AuthorInDB:
        if type(author_id) == str:
            author_id = UUID(author_id)
        with self.session_factory() as session:
            return session.query(AuthorInDB).filter_by(id=author_id).first()

    def update(self, author_id: UUID, author_new: AuthorInUpdate) -> AuthorInDB:
        if type(author_id) == str:
            author_id = UUID(author_id)
        with self.session_factory() as session:
            author = session.query(AuthorInDB).filter_by(id=author_id).first()
            for key, value in author_new.dict(exclude_unset=True).items():
                setattr(author, key, value)
            session.commit()
            session.refresh(author)
            return author

    def delete(self, author_id: UUID) -> None:
        if type(author_id) == str:
            author_id = UUID(author_id)
        with self.session_factory() as session:
            author = session.query(AuthorInDB).filter_by(id=author_id).first()
            session.delete(author)
            session.commit()
            return None
