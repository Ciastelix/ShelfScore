from fastapi import APIRouter, status, Depends
from schemas.user import UserInCreate, UserInResponse, UserInUpdate
from dependency_injector.wiring import Provide, inject
from services.user import UserService
from container import Container
from uuid import UUID
from fastapi.security import OAuth2PasswordRequestForm
from services.auth import AuthService
from fastapi import HTTPException
from repositories.auth import oauth2_scheme

router = APIRouter()


@router.get("/", response_model=list[UserInResponse], status_code=status.HTTP_200_OK)
@inject
def read_users(user_service: UserService = Depends(Provide[Container.user_service])):
    return user_service.get_all()


@router.post("/", response_model=UserInResponse, status_code=status.HTTP_201_CREATED)
@inject
def create_user(
    user: UserInCreate,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.add(user)


@router.get("/{user_id}", response_model=UserInResponse, status_code=status.HTTP_200_OK)
@inject
def read_user(
    user_id: UUID, user_service: UserService = Depends(Provide[Container.user_service])
):
    return user_service.get_by_id(user_id)


@router.put("/{user_id}", response_model=UserInResponse, status_code=status.HTTP_200_OK)
@inject
def update_user(
    user_id: UUID,
    user: UserInUpdate,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    return user_service.update(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_user(
    user_id: UUID, user_service: UserService = Depends(Provide[Container.user_service])
):
    return user_service.delete(user_id)


@router.post(
    "/login",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
@inject
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    return auth_service.login(form_data.username, form_data.password)


@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    user = auth_service.get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.get(
    "/me/token",
    status_code=status.HTTP_200_OK,
    tags=["users"],
)
@inject
async def read_users_me(current_user=Depends(get_current_user)):

    return {"user": current_user, "isValid": True}
