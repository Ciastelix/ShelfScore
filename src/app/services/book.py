from schemas.book import BookInCreate, BookInUpdate
from models.book import Book
from repositories.book import BookRepository
from uuid import UUID
from fastapi import UploadFile


class BookService:
    def __init__(self, book_repository: BookRepository) -> None:
        self.book_repository = book_repository

    def add(self, book: BookInCreate, image: UploadFile) -> Book:
        return self.book_repository.add(book, image)

    def get_all(self) -> list[Book]:
        return self.book_repository.get_all()

    def get_by_id(self, book_id: UUID) -> Book:
        return self.book_repository.get_by_id(book_id)

    def update(self, book_id: UUID, book_new: BookInUpdate) -> Book:
        return self.book_repository.update(book_id, book_new)

    def delete(self, book_id: UUID) -> None:
        return self.book_repository.delete(book_id)
