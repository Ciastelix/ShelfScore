from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from ..schemas.review import ReviewInCreate, ReviewInUpdate
from ..models.review import Review
from uuid import UUID


class ReviewRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def add(self, review: ReviewInCreate) -> Review:
        with self.session_factory() as session:
            obj = Review(**review.model_dump())
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def get_all(self, offset: int, limit: int, filter: str) -> list[Review]:
        with self.session_factory() as session:
            q = session.query(Review)
            if filter:
                q = q.filter(Review.review.ilike(f"%{filter}%"))
            return q.offset(offset).limit(limit).all()

    def get_by_id(self, review_id: UUID) -> Review | None:
        with self.session_factory() as session:
            return session.query(Review).filter_by(id=review_id).first()

    def update(self, review_id: UUID, review_new: ReviewInUpdate) -> Review:
        with self.session_factory() as session:
            obj = session.query(Review).filter_by(id=review_id).first()
            for k, v in review_new.model_dump(exclude_unset=True).items():
                setattr(obj, k, v)
            session.commit()
            session.refresh(obj)
            return obj

    def delete(self, review_id: UUID) -> None:
        with self.session_factory() as session:
            obj = session.query(Review).filter_by(id=review_id).first()
            if obj:
                session.delete(obj)
                session.commit()
