import os
import io
from types import SimpleNamespace
from pathlib import Path
from uuid import UUID
from unittest.mock import MagicMock, AsyncMock

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from dependency_injector.wiring import Provide
from dependency_injector import providers

# Set env before importing app/container
ROOT = Path(__file__).resolve().parents[3]
os.environ.setdefault("DB_URL", f"sqlite:///{ROOT}/src/app/db.sqlite3")
os.environ.setdefault("JWT_SECRET", "fJJZNs9LnU356LmyTQA8")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("IMAGE_URL", f"{ROOT}/shelf/public/images")

from app.container import Container
from app.main import app
from app.schemas.user import UserInCreate, UserInUpdate, UserUpdatePassword
from app.utils.current_user import get_current_user

client = TestClient(app)

USER_ID = str(UUID("11111111-1111-1111-1111-111111111111"))

MOCK_USER = {
    "id": USER_ID,
    "username": "john",
    "email": "john@example.com",
    "description": "",
    "picture": "default.png",
    "is_active": True,
}

@pytest.fixture(autouse=True)
def mock_current_user():
    # Object with .id for endpoints that access attribute
    current = SimpleNamespace(id=UUID(USER_ID))
    app.dependency_overrides[get_current_user] = lambda: current
    yield
    app.dependency_overrides.pop(get_current_user, None)

@pytest.fixture
def mock_user_service():
    svc = MagicMock()
    app.dependency_overrides[Provide[Container.user_service]] = lambda: svc
    app.container.user_service.override(providers.Object(svc))
    yield svc
    app.dependency_overrides.pop(Provide[Container.user_service], None)
    app.container.user_service.reset_override()

@pytest.fixture
def mock_auth_service():
    svc = MagicMock()
    app.dependency_overrides[Provide[Container.auth_service]] = lambda: svc
    app.container.auth_service.override(providers.Object(svc))
    yield svc
    app.dependency_overrides.pop(Provide[Container.auth_service], None)
    app.container.auth_service.reset_override()

@pytest.fixture
def mock_image_service():
    svc = MagicMock()
    svc.save_image = AsyncMock()
    app.dependency_overrides[Provide[Container.image_service]] = lambda: svc
    app.container.image_service.override(providers.Object(svc))
    yield svc
    app.dependency_overrides.pop(Provide[Container.image_service], None)
    app.container.image_service.reset_override()

def test_create_user(mock_user_service: MagicMock):
    mock_user_service.add.return_value = MOCK_USER
    payload = UserInCreate(username="john", email="john@example.com", password="secret")
    resp = client.post("/users/", json=payload.model_dump())
    assert resp.status_code == 201
    assert resp.json() == MOCK_USER

def test_read_users(mock_user_service: MagicMock):
    mock_user_service.get_all.return_value = [MOCK_USER]
    resp = client.get("/users/")
    assert resp.status_code == 200
    assert resp.json() == [MOCK_USER]

def test_read_user(mock_user_service: MagicMock):
    mock_user_service.get_by_id.return_value = MOCK_USER
    resp = client.get(f"/users/u/{USER_ID}")
    assert resp.status_code == 200
    assert resp.json() == MOCK_USER

def test_update_user(mock_user_service: MagicMock):
    update = UserInUpdate(
        username="johnny",
        email="johnny@example.com",
        description="hi",
        picture="profiles/pic.png",
        is_active=True,
    )
    expected = {**MOCK_USER, **update.model_dump(exclude_unset=True)}
    mock_user_service.update.return_value = expected
    resp = client.put(f"/users/{USER_ID}", json=update.model_dump(exclude_unset=True))
    assert resp.status_code == 200
    assert resp.json() == expected

def test_delete_user(mock_user_service: MagicMock):
    mock_user_service.delete.return_value = None
    resp = client.delete(f"/users/{USER_ID}")
    assert resp.status_code == 204

def test_login_user(mock_auth_service: MagicMock):
    token = {"access_token": "token123", "token_type": "bearer"}
    mock_auth_service.login.return_value = token
    # OAuth2PasswordRequestForm expects form-encoded data
    resp = client.post(
        "/users/login",
        data={"username": "john@example.com", "password": "secret", "grant_type": "password"},
    )
    assert resp.status_code == 200
    assert resp.json() == token

def test_change_password(mock_user_service: MagicMock):
    mock_user_service.change_password.return_value = None
    payload = UserUpdatePassword(password="old", new_password="new")
    resp = client.post("/users/change-password", json=payload.model_dump())
    assert resp.status_code == 200

def test_upload_image(mock_user_service: MagicMock, mock_image_service: MagicMock):
    # valid in-memory PNG
    buf = io.BytesIO()
    Image.new("RGB", (4, 4)).save(buf, format="PNG")
    buf.seek(0)

    mock_image_service.save_image.return_value = "profiles/11111111-1111-1111-1111-111111111111.png"
    expected = {**MOCK_USER, "picture": mock_image_service.save_image.return_value}
    mock_user_service.add_image.return_value = expected

    files = {"file": ("pic.png", buf.getvalue(), "image/png")}
    resp = client.post("/users/upload-image", files=files)
    assert resp.status_code == 200
    assert resp.json() == expected

def test_me_token():
    resp = client.get("/users/me/token")
    assert resp.status_code == 200
    body = resp.json()
    assert body["isValid"] is True
    # current_user has id only; ensure it is serialized as a string UUID
    assert str(UUID(USER_ID)) == str(body["user"]["id"])

def test_get_books_read_by_user_with_author(mock_user_service: MagicMock):
    books = [
        {
            "id": "aaaaaaaa-1111-2222-3333-bbbbbbbbbbbb",
            "title": "Title",
            "genre": "Genre",
            "year": 2020,
            "description": "Desc",
            "image": "img.png",
            "is_active": True,
            "author_name": "John",
            "author_surname": "Doe",
        }
    ]
    mock_user_service.get_books_read_by_user_with_author.return_value = books
    resp = client.get(f"/users/books-read?user_id={USER_ID}")
    assert resp.status_code == 200
    assert resp.json() == books