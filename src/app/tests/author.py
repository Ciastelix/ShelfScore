import io
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from dependency_injector.wiring import Provide
from app.container import Container
from app.main import app
from app.schemas.author import AuthorInCreate, AuthorInUpdate


client = TestClient(app)
MOCK_AUTHOR_ID = None

MOCK_AUTHOR = {
    "id": None,
    "name": "John",
    "surname": "Doe",
    "description": "Author of books",
    "is_active": True,
    "year_born": "1970",
    "photo": "default.png",
}


@pytest.fixture
def mock_author_service():
    svc = MagicMock()
    app.dependency_overrides[Provide[Container.author_service]] = lambda: svc
    yield svc
    app.dependency_overrides.pop(Provide[Container.author_service], None)


def test_create_author(mock_author_service):
    global MOCK_AUTHOR_ID
    mock_author_service.add.return_value = MOCK_AUTHOR

    author_data = AuthorInCreate(
        name="John",
        surname="Doe",
        description="Author of books",
        year_born="1970",
    )
    response = client.post("/authors/", json=author_data.model_dump())
    assert response.status_code == 201

    MOCK_AUTHOR_ID = response.json().get("id")
    MOCK_AUTHOR["id"] = MOCK_AUTHOR_ID
    MOCK_AUTHOR["photo"] = response.json().get("photo")
    assert response.json() == MOCK_AUTHOR


def test_read_authors(mock_author_service):
    mock_author_service.get_all.return_value = [MOCK_AUTHOR]
    response = client.get("/authors/")
    assert response.status_code == 200
    assert response.json() == [MOCK_AUTHOR]


def test_read_author(mock_author_service):
    mock_author_service.get_by_id.return_value = MOCK_AUTHOR
    response = client.get(f"/authors/{MOCK_AUTHOR_ID}")
    assert response.status_code == 200
    assert response.json() == MOCK_AUTHOR


def test_update_author(mock_author_service):
    mock_author_service.update.return_value = MOCK_AUTHOR

    author_update = AuthorInUpdate(
        name="Jane",
        surname="Doe",
        description="Updated bio",
        is_active=True,
        year_born="1980",
    )
    response = client.put(
        f"/authors/{MOCK_AUTHOR_ID}",
        json=author_update.model_dump(exclude_unset=True),
    )
    assert response.status_code == 200
    MOCK_AUTHOR.update(author_update.model_dump(exclude_unset=True))
    assert response.json() == MOCK_AUTHOR


def test_update_author_image(mock_author_service):
    buf = io.BytesIO()
    Image.new("RGB", (4, 4), color=(255, 0, 0)).save(buf, format="PNG")
    buf.seek(0)

    updated = {**MOCK_AUTHOR, "photo": f"authors/{MOCK_AUTHOR_ID}.png"}
    mock_author_service.update_image.return_value = updated

    files = {"image": ("image.png", buf.getvalue(), "image/png")}
    response = client.patch(f"/authors/{MOCK_AUTHOR_ID}/image", files=files)
    assert response.status_code == 200
    assert response.json() == updated


def test_delete_author(mock_author_service):
    mock_author_service.delete.return_value = None
    response = client.delete(f"/authors/{MOCK_AUTHOR_ID}")
    assert response.status_code == 204
