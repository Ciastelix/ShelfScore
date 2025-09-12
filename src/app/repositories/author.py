from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..schemas.author import AuthorInCreate, AuthorInDB, AuthorInUpdate
from ..models.author import Author
from uuid import UUID
from fastapi import UploadFile
from ..services.image import ImageService
from pathlib import Path


class AuthorRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
        image_service: ImageService,
    ) -> None:
        self.session_factory = session_factory
        self.image_service = image_service

    def add(self, author: AuthorInCreate) -> AuthorInDB:
        with self.session_factory() as session:
            author = Author(**author.model_dump())
            session.add(author)
            session.commit()
            session.refresh(author)
        return author

    def get_all(
        self, offset: int, limit: int, filter: str
    ) -> list[AuthorInDB]:
        with self.session_factory() as session:
            if not filter:
                return session.query(Author).offset(offset).limit(limit).all()
            return (
                session.query(Author)
                .filter(Author.name.ilike(f"%{filter}%"))
                .offset(offset)
                .limit(limit)
                .all()
            )

    def get_by_id(self, author_id: UUID) -> AuthorInDB:
        if isinstance(author_id, str):
            author_id = UUID(author_id)
        with self.session_factory() as session:
            return session.query(Author).filter_by(id=author_id).first()

    def update(
        self, author_id: UUID, author_new: AuthorInUpdate
    ) -> AuthorInDB:
        if isinstance(author_id, str):
            author_id = UUID(author_id)
        with self.session_factory() as session:
            author = session.query(Author).filter_by(id=author_id).first()
            for key, value in author_new.model_dump(
                exclude_unset=True
            ).items():
                setattr(author, key, value)
            session.commit()
            session.refresh(author)
            return author

    async def update_image(
        self, author_id: UUID, image: UploadFile
    ) -> AuthorInDB:
        if isinstance(author_id, str):
            author_id = UUID(author_id)
        with self.session_factory() as session:
            author = session.query(Author).filter_by(id=author_id).first()
            image_path = await self.image_service.save_image(
                author.id, image, "authors", 200, 200
            )
            p = Path(image_path)
            base = Path(getattr(self.image_service, "upload_dir", ""))
            try:
                rel = p.relative_to(base)
                author.photo = rel.as_posix()
            except Exception:
                parts = p.parts
                if "authors" in parts:
                    idx = parts.index("authors")
                    author.photo = Path(*parts[idx:]).as_posix()
                else:
                    author.photo = p.name
            session.commit()
            session.refresh(author)
            return author

    def delete(self, author_id: UUID) -> None:
        if isinstance(author_id, str):
            author_id = UUID(author_id)
        with self.session_factory() as session:
            author = session.query(Author).filter_by(id=author_id).first()
            if author:
                session.delete(author)
                session.commit()
