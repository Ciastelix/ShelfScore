from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide, inject
from services.author import AuthorService
from container import Container
from uuid import UUID
from schemas.author import AuthorInDB, AuthorInCreate, AuthorInUpdate
from typing import List

router = APIRouter()


@router.get("/", response_model=List[AuthorInDB], status_code=status.HTTP_200_OK)
@inject
def read_authors(
    offset: int = 0,
    limit: int = 10,
    filter: str = "",
    author_service: AuthorService = Depends(Provide[Container.author_service]),
) -> List[AuthorInDB]:
    return author_service.get_all(offset, limit, filter)


@router.post("/", response_model=AuthorInDB, status_code=status.HTTP_201_CREATED)
@inject
def create_author(
    author: AuthorInCreate,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
) -> AuthorInDB:
    return author_service.add(author)


@router.get("/{author_id}", response_model=AuthorInDB, status_code=status.HTTP_200_OK)
@inject
def read_author(
    author_id: UUID,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
) -> AuthorInDB:
    return author_service.get_by_id(author_id)


@router.patch(
    "/{author_id}/image", response_model=AuthorInDB, status_code=status.HTTP_200_OK
)
@inject
def update_author_image(
    author_id: UUID,
    image: str,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
) -> AuthorInDB:
    return author_service.update_image(author_id, image)


@router.put("/{author_id}", response_model=AuthorInDB, status_code=status.HTTP_200_OK)
@inject
def update_author(
    author_id: UUID,
    author: AuthorInUpdate,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
) -> AuthorInDB:
    return author_service.update(author_id, author)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_author(
    author_id: UUID,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
) -> None:
    return author_service.delete(author_id)
