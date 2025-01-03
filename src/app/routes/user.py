from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File
from schemas.user import UserInCreate, UserInDB, UserInUpdate, UserUpdatePassword
from dependency_injector.wiring import Provide, inject
from services.user import UserService
from container import Container
from uuid import UUID
from fastapi.security import OAuth2PasswordRequestForm
from services.auth import AuthService
from utils.current_user import get_current_user
from services.image import ImageService
from typing import List, Dict, Any

router = APIRouter()


@router.get("/", response_model=List[UserInDB], status_code=status.HTTP_200_OK)
@inject
def read_users(
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> List[UserInDB]:
    return user_service.get_all()


@router.post("/", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
@inject
def create_user(
    user: UserInCreate,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> UserInDB:
    return user_service.add(user)


@router.get("/{user_id}", response_model=UserInDB, status_code=status.HTTP_200_OK)
@inject
def read_user(
    user_id: UUID, user_service: UserService = Depends(Provide[Container.user_service])
) -> UserInDB:
    return user_service.get_by_id(user_id)


@router.put("/{user_id}", response_model=UserInDB, status_code=status.HTTP_200_OK)
@inject
def update_user(
    user_id: UUID,
    user: UserInUpdate,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> UserInDB:
    return user_service.update(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_user(
    user_id: UUID, user_service: UserService = Depends(Provide[Container.user_service])
) -> None:
    return user_service.delete(user_id)


@router.post(
    "/login",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
@inject
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> Dict[str, Any]:
    return auth_service.login(form_data.username, form_data.password)


@router.post("/change-password", status_code=status.HTTP_200_OK)
@inject
def change_password(
    user: UserUpdatePassword,
    user_service: UserService = Depends(Provide[Container.user_service]),
    current_user=Depends(get_current_user),
) -> None:
    return user_service.change_password(user, current_user)


@router.post("/upload-image", response_model=UserInDB, status_code=status.HTTP_200_OK)
@inject
async def upload_image(
    current_user=Depends(get_current_user),
    file: UploadFile = File(...),
    user_service: UserService = Depends(Provide[Container.user_service]),
    image_service: ImageService = Depends(Provide[Container.image_service]),
) -> UserInDB:
    # Check if the uploaded file is an image
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format")

    # Save the image and get the path
    image_path = await image_service.save_image(current_user.id, file, 100, 100)

    # Update the user's picture in the database
    user = user_service.add_image(current_user.id, image_path)

    return user


@router.get(
    "/me/token",
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
@inject
async def read_users_me(current_user=Depends(get_current_user)):
    return {"user": current_user, "isValid": True}
