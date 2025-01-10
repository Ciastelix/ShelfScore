from fastapi import Depends, HTTPException, status
from services.auth import AuthService
from dependency_injector.wiring import Provide, inject
from container import Container
from repositories.auth import oauth2_scheme


@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    user = auth_service.get_current_user(token)
    print(user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
