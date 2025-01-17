from contextlib import contextmanager, AbstractContextManager
from typing import Callable
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

# Import all models here
from models.user import User
from models.book import Book
from models.review import Review
from models.author import Author


class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=False)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:  # type: ignore
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
