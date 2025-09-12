import io
from uuid import UUID
from unittest.mock import MagicMock, AsyncMock
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from dependency_injector import providers
from dependency_injector.wiring import Provide

from app.container import Container
from app.main import app
from app.schemas.book import BookInCreate, BookInUpdate
from app.utils.current_user import get_current_user

client = TestClient(app)

BOOK_ID = str(UUID("12345678-1234-5678-1234-567812345678"))
AUTHOR_ID = str(UUID("87654321-4321-6789-4321-678987654321"))

MOCK_BOOK = {
    "id": BOOK_ID,
    "title": "My Book",
    "author_id": AUTHOR_ID,
    "genre": "Fiction",
    "year": 2023,
    "description": "Nice book",
    "image": "default.png",
    "is_active": True,
}


@pytest.fixture(autouse=True)
def mock_user():
    app.dependency_overrides[get_current_user] = lambda: {"id": "user-1"}
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def mock_book_service():
    svc = MagicMock()
    # async endpoints need awaitables:
    svc.add = AsyncMock()
    svc.update_image = AsyncMock()
    # optional sync methods:
    # svc.get_all, svc.get_by_id, svc.update, svc.delete are fine as MagicMock
    app.dependency_overrides[Provide[Container.book_service]] = lambda: svc
    # also override the provider to be extra safe
    app.container.book_service.override(providers.Object(svc))
    yield svc
    app.dependency_overrides.pop(Provide[Container.book_service], None)
    app.container.book_service.reset_override()


def test_create_book(mock_book_service: MagicMock):
    mock_book_service.add.return_value = MOCK_BOOK
    payload = BookInCreate(
        title="My Book",
        author_id=UUID(AUTHOR_ID),
        genre="Fiction",
        year=2023,
        description="Nice book",
    )
    resp = client.post("/books/", json=payload.model_dump(mode="json"))

    assert resp.status_code == 201
    assert resp.json() == MOCK_BOOK


def test_read_books(mock_book_service: MagicMock):
    mock_book_service.get_all.return_value = [MOCK_BOOK]
    resp = client.get("/books/?offset=0&limit=10&filter=")
    assert resp.status_code == 200
    assert resp.json() == [MOCK_BOOK]


def test_read_book(mock_book_service: MagicMock):
    mock_book_service.get_by_id.return_value = MOCK_BOOK
    resp = client.get(f"/books/{BOOK_ID}")
    assert resp.status_code == 200
    assert resp.json() == MOCK_BOOK


def test_update_book(mock_book_service: MagicMock):
    update = BookInUpdate(
        title="My Book 2",
        genre="Drama",
        year=2024,
        description="Updated",
        is_active=True,
    )
    expected = {**MOCK_BOOK, **update.model_dump(exclude_unset=True)}
    mock_book_service.update.return_value = expected
    resp = client.put(
        f"/books/{BOOK_ID}",
        json=update.model_dump(exclude_unset=True),
    )
    assert resp.status_code == 200
    assert resp.json() == expected


def test_update_book_image(mock_book_service: MagicMock):
    buf = io.BytesIO()
    Image.new("RGB", (4, 4), color=(0, 255, 0)).save(buf, format="PNG")
    buf.seek(0)

    expected = {**MOCK_BOOK, "image": f"books/{BOOK_ID}.png"}
    mock_book_service.update_image.return_value = expected

    files = {"image": ("cover.png", buf.getvalue(), "image/png")}
    resp = client.put(f"/books/{BOOK_ID}/image", files=files)
    assert resp.status_code == 200
    assert resp.json() == expected


def test_delete_book(mock_book_service: MagicMock):
    mock_book_service.delete.return_value = None
    resp = client.delete(f"/books/{BOOK_ID}")
    assert resp.status_code == 204
