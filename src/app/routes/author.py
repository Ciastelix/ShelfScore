from fastapi import APIRouter, Depends, status
from fastapi import APIRouter, status, Depends
from dependency_injector.wiring import Provide, inject
from services.author import AuthorService
from container import Container
from uuid import UUID
from fastapi.security import OAuth2PasswordRequestForm
from services.auth import AuthService
from fastapi import HTTPException
from repositories.auth import oauth2_scheme
from utils.current_user import get_current_user
from fastapi import UploadFile, File
from services.image import ImageService
from schemas.author import AuthorInDB, AuthorInCreate, AuthorInUpdate
from services.author import AuthorService

router = APIRouter()


@router.get("/", response_model=list[AuthorInDB], status_code=status.HTTP_200_OK)
@inject
def read_authors(
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    return author_service.get_all()


@router.post("/", response_model=AuthorInDB, status_code=status.HTTP_201_CREATED)
@inject
def create_author(
    author: AuthorInCreate,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    return author_service.add(author)


@router.get("/{author_id}", response_model=AuthorInDB, status_code=status.HTTP_200_OK)
@inject
def read_author(
    author_id: UUID,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    return author_service.get_by_id(author_id)


@router.put("/{author_id}", response_model=AuthorInDB, status_code=status.HTTP_200_OK)
@inject
def update_author(
    author_id: UUID,
    author: AuthorInUpdate,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    return author_service.update(author_id, author)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_author(
    author_id: UUID,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    return author_service.delete(author_id)
