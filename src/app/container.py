from dependency_injector import containers, providers
from db import Database
from services.user import UserService
from services.auth import AuthService
from repositories.auth import AuthRepository
from repositories.user import UserRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["routes.user"])
    config = providers.Configuration()
    config.db.url.from_env("DB_URL")
    db = providers.Singleton(Database, db_url=config.db.url)

    user_repository = providers.Singleton(
        UserRepository, session_factory=db.provided.session
    )

    user_service = providers.Factory(UserService, user_repository=user_repository)

    auth_repository = providers.Singleton(
        AuthRepository, session_factory=db.provided.session
    )

    auth_service = providers.Factory(AuthService, auth_repository=auth_repository)
