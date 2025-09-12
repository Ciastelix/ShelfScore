from dependency_injector import containers, providers
from pathlib import Path
from .db import Database
from .services.user import UserService
from .services.auth import AuthService
from .services.author import AuthorService
from .services.review import ReviewService
from .services.book import BookService
from .services.image import ImageService
from .repositories.author import AuthorRepository
from .repositories.review import ReviewRepository
from .repositories.book import BookRepository
from .repositories.auth import AuthRepository
from .repositories.user import UserRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.routes"])

    config = providers.Configuration()

    _APP_DIR = Path(__file__).resolve().parent
    _ROOT_DIR = _APP_DIR.parent.parent
    config.db.url.from_env(
        "DB_URL", default=f"sqlite:///{_APP_DIR / 'db.sqlite3'}"
    )
    config.image.upload_dir.from_env(
        "IMAGE_URL", default=str(_ROOT_DIR / "shelf" / "public" / "images")
    )

    db = providers.Singleton(Database, db_url=config.db.url)

    image_service = providers.Factory(
        ImageService, upload_dir=config.image.upload_dir
    )

    user_repository = providers.Singleton(
        UserRepository, session_factory=db.provided.session
    )
    book_repository = providers.Singleton(
        BookRepository,
        session_factory=db.provided.session,
        image_service=image_service,
    )
    review_repository = providers.Singleton(
        ReviewRepository, session_factory=db.provided.session
    )
    author_repository = providers.Factory(
        AuthorRepository,
        session_factory=db.provided.session,
        image_service=image_service,
    )
    auth_repository = providers.Singleton(
        AuthRepository, session_factory=db.provided.session
    )

    user_service = providers.Factory(
        UserService, user_repository=user_repository
    )
    book_service = providers.Factory(
        BookService, book_repository=book_repository
    )
    review_service = providers.Factory(
        ReviewService, review_repository=review_repository
    )
    author_service = providers.Factory(
        AuthorService, author_repository=author_repository
    )
    auth_service = providers.Factory(
        AuthService, auth_repository=auth_repository
    )
