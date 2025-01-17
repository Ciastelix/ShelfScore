from schemas.author import AuthorInCreate, AuthorInDB, AuthorInUpdate
from uuid import UUID
from repositories.author import AuthorRepository


class AuthorService:
    def __init__(self, author_repository: AuthorRepository) -> None:
        self.author_repository = author_repository

    def add(self, author: AuthorInCreate) -> AuthorInDB:
        return self.author_repository.add(author)

    def get_all(self, offset: int, limit: int, filter: str) -> list[AuthorInDB]:
        return self.author_repository.get_all(offset, limit, filter)

    def get_by_id(self, author_id: UUID) -> AuthorInDB:
        return self.author_repository.get_by_id(author_id)

    async def update_image(self, author_id: UUID, image: str) -> AuthorInDB:
        return self.author_repository.update_image(author_id, image)

    def update(self, author_id: UUID, author_new: AuthorInUpdate) -> AuthorInDB:
        return self.author_repository.update(author_id, author_new)

    def delete(self, author_id: UUID) -> None:
        return self.author_repository.delete(author_id)
