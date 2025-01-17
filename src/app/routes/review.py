from fastapi import APIRouter, status, Depends
from schemas.review import ReviewInCreate, ReviewInDB, ReviewInUpdate
from dependency_injector.wiring import Provide, inject
from services.review import ReviewService
from container import Container
from uuid import UUID
from typing import List
from utils.current_user import get_current_user

router = APIRouter()


@router.get("/", response_model=List[ReviewInDB], status_code=status.HTTP_200_OK)
@inject
def read_reviews(
    offset: int = 0,
    limit: int = 10,
    filter: str = "",
    review_service: ReviewService = Depends(Provide[Container.review_service]),
) -> List[ReviewInDB]:
    return review_service.get_all(offset, limit, filter)


@router.post("/", response_model=ReviewInDB, status_code=status.HTTP_201_CREATED)
@inject
async def create_review(
    review: ReviewInCreate,
    review_service: ReviewService = Depends(Provide[Container.review_service]),
    user=Depends(get_current_user),
) -> ReviewInDB:
    return review_service.add(review)


@router.get("/{review_id}", response_model=ReviewInDB, status_code=status.HTTP_200_OK)
@inject
def read_review(
    review_id: UUID,
    review_service: ReviewService = Depends(Provide[Container.review_service]),
) -> ReviewInDB:
    return review_service.get_by_id(review_id)


@router.put("/{review_id}", response_model=ReviewInDB, status_code=status.HTTP_200_OK)
@inject
async def update_review(
    review_id: UUID,
    review: ReviewInUpdate,
    review_service: ReviewService = Depends(Provide[Container.review_service]),
    user=Depends(get_current_user),
) -> ReviewInDB:
    return review_service.update(review_id, review)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_review(
    review_id: UUID,
    review_service: ReviewService = Depends(Provide[Container.review_service]),
    user=Depends(get_current_user),
) -> None:
    return review_service.delete(review_id)
