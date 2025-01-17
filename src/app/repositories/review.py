from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from schemas.review import ReviewInCreate, ReviewInUpdate
from models.review import Review
from uuid import UUID


class ReviewRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def add(self, review: ReviewInCreate) -> Review:
        with self.session_factory() as session:
            review = Review(**review.model_dump())
            session.add(review)
            session.commit()
            session.refresh(review)
        return review

    def get_all(self, offset: int, limit: int) -> list[Review]:
        with self.session_factory() as session:
            return session.query(Review).offset(offset).limit(limit).all()

    def get_by_id(self, review_id: UUID) -> Review:
        if type(review_id) == str:
            review_id = UUID(review_id)
        with self.session_factory() as session:
            return session.query(Review).filter_by(id=review_id).first()

    def update(self, review_id: UUID, review_new: ReviewInUpdate) -> Review:
        if type(review_id) == str:
            review_id = UUID(review_id)
        with self.session_factory() as session:
            review = session.query(Review).filter_by(id=review_id).first()
            for key, value in review_new.model_dump().items():
                setattr(review, key, value)
            session.commit()
            session.refresh(review)
            return review

    def delete(self, review_id: UUID) -> None:
        if type(review_id) == str:
            review_id = UUID(review_id)
        with self.session_factory() as session:
            review = session.query(Review).filter_by(id=review_id).first()
            session.delete(review)
            session.commit()
