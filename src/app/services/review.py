from schemas.review import ReviewInCreate, ReviewInUpdate
from models.review import Review
from repositories.review import ReviewRepository
from uuid import UUID


class ReviewService:
    def __init__(self, review_repository: ReviewRepository) -> None:
        self.review_repository = review_repository

    def add(self, review: ReviewInCreate) -> Review:
        return self.review_repository.add(review)

    def get_all(self, offset: int, limit: int, filter: str) -> list[Review]:
        return self.review_repository.get_all(offset, limit, filter)

    def get_by_id(self, review_id: UUID) -> Review:
        return self.review_repository.get_by_id(review_id)

    def update(self, review_id: UUID, review_new: ReviewInUpdate) -> Review:
        return self.review_repository.update(review_id, review_new)

    def delete(self, review_id: UUID) -> None:
        return self.review_repository.delete(review_id)
