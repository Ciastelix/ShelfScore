from fastapi import APIRouter, status, Depends, UploadFile, File
from schemas.book import BookInCreate, BookInDB, BookInUpdate
from dependency_injector.wiring import Provide, inject
from services.book import BookService
from container import Container
from uuid import UUID
from utils.current_user import get_current_user
from typing import List


router = APIRouter()


@router.get("/", response_model=List[BookInDB], status_code=status.HTTP_200_OK)
@inject
def read_books(
    offset: int = 0,
    limit: int = 10,
    filter: str = "",
    book_service: BookService = Depends(Provide[Container.book_service]),
) -> List[BookInDB]:
    return book_service.get_all(offset, limit, filter)


@router.post("/", response_model=BookInDB, status_code=status.HTTP_201_CREATED)
@inject
async def create_book(
    book: BookInCreate,
    book_service: BookService = Depends(Provide[Container.book_service]),
    user=Depends(get_current_user),
) -> BookInDB:
    return await book_service.add(book)


@router.put("/{book_id}/image", status_code=status.HTTP_200_OK)
@inject
async def update_image(
    book_id: UUID,
    image: UploadFile = File(...),
    book_service: BookService = Depends(Provide[Container.book_service]),
    user=Depends(get_current_user),
):
    return await book_service.update_image(book_id, image)


@router.get("/{book_id}", response_model=BookInDB, status_code=status.HTTP_200_OK)
@inject
def read_book(
    book_id: UUID, book_service: BookService = Depends(Provide[Container.book_service])
) -> BookInDB:
    return book_service.get_by_id(book_id)


@router.put("/{book_id}", response_model=BookInDB, status_code=status.HTTP_200_OK)
@inject
def update_book(
    book_id: UUID,
    book: BookInUpdate,
    book_service: BookService = Depends(Provide[Container.book_service]),
    user=Depends(get_current_user),
) -> BookInDB:
    return book_service.update(book_id, book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_book(
    book_id: UUID,
    book_service: BookService = Depends(Provide[Container.book_service]),
    user=Depends(get_current_user),
) -> None:
    return book_service.delete(book_id)
