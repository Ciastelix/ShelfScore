from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from schemas.book import BookInCreate, BookInUpdate
from models.book import Book
from uuid import UUID
from services.image import ImageService
from fastapi import UploadFile


class BookRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
        image_service: ImageService,
    ) -> None:
        self.session_factory = session_factory
        self.image_service = image_service

    async def add(self, book: BookInCreate) -> Book:
        with self.session_factory() as session:
            book_data = book.model_dump()
            book = Book(**book_data)
            session.add(book)
            session.commit()
            session.refresh(book)
        return book

    async def update_image(self, book_id: UUID, image: UploadFile) -> Book:
        if type(book_id) == str:
            book_id = UUID(book_id)
        with self.session_factory() as session:
            book = session.query(Book).filter_by(id=book_id).first()
            image_path = await self.image_service.save_image(
                book.id, image, "books", 200, 300
            )

            book.image = "/".join(image_path.split("/")[3:])
            session.commit()
            session.refresh(book)
            return book

    def get_all(self, offset: int, limit: int, filter: str) -> list[Book]:
        with self.session_factory() as session:
            if not filter:
                return session.query(Book).offset(offset).limit(limit).all()
            return (
                session.query(Book)
                .filter(Book.title.ilike(f"%{filter}%"))
                .offset(offset)
                .limit(limit)
                .all()
            )

    def get_by_id(self, book_id: UUID) -> Book:
        if type(book_id) == str:
            book_id = UUID(book_id)
        with self.session_factory() as session:
            return session.query(Book).filter_by(id=book_id).first()

    def update(self, book_id: UUID, book_new: BookInUpdate) -> Book:
        if type(book_id) == str:
            book_id = UUID(book_id)
        with self.session_factory() as session:
            book = session.query(Book).filter_by(id=book_id).first()
            for key, value in book_new.model_dump().items():
                setattr(book, key, value)
            session.commit()
            session.refresh(book)
            return book

    def delete(self, book_id: UUID) -> None:
        if type(book_id) == str:
            book_id = UUID(book_id)
        with self.session_factory() as session:
            book = session.query(Book).filter_by(id=book_id).first()
            session.delete(book)
            session.commit()
