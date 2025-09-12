from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..schemas.book import BookInCreate, BookInUpdate
from ..models.book import Book
from uuid import UUID
from ..services.image import ImageService
from fastapi import UploadFile
from pathlib import Path


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
            obj = Book(**book.model_dump())
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def get_all(self, offset: int, limit: int, filter: str) -> list[Book]:
        with self.session_factory() as session:
            q = session.query(Book)
            if filter:
                q = q.filter(Book.title.ilike(f"%{filter}%"))
            return q.offset(offset).limit(limit).all()

    def get_by_id(self, book_id: UUID) -> Book:
        with self.session_factory() as session:
            return session.query(Book).filter_by(id=book_id).first()

    def update(self, book_id: UUID, book_new: BookInUpdate) -> Book:
        with self.session_factory() as session:
            obj = session.query(Book).filter_by(id=book_id).first()
            for k, v in book_new.model_dump(exclude_unset=True).items():
                setattr(obj, k, v)
            session.commit()
            session.refresh(obj)
            return obj

    async def update_image(self, book_id: UUID, image: UploadFile) -> Book:
        with self.session_factory() as session:
            obj = session.query(Book).filter_by(id=book_id).first()
            image_path = await self.image_service.save_image(
                obj.id, image, "books", 400, 600
            )
            p = Path(image_path)
            base = Path(getattr(self.image_service, "upload_dir", ""))
            try:
                rel = p.relative_to(base)
                obj.image = rel.as_posix()
            except Exception:
                parts = p.parts
                if "books" in parts:
                    idx = parts.index("books")
                    obj.image = Path(*parts[idx:]).as_posix()
                else:
                    obj.image = p.name
            session.commit()
            session.refresh(obj)
            return obj

    def delete(self, book_id: UUID) -> None:
        with self.session_factory() as session:
            obj = session.query(Book).filter_by(id=book_id).first()
            if obj:
                session.delete(obj)
                session.commit()
