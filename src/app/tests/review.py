from uuid import UUID
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from dependency_injector.wiring import Provide
from dependency_injector import providers

from app.container import Container
from app.main import app
from app.schemas.review import ReviewInCreate, ReviewInUpdate
from app.utils.current_user import get_current_user

client = TestClient(app)

REVIEW_ID = str(UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"))
USER_ID = str(UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"))
BOOK_ID = str(UUID("cccccccc-cccc-cccc-cccc-cccccccccccc"))

MOCK_REVIEW = {
    "id": REVIEW_ID,
    "user_id": USER_ID,
    "book_id": BOOK_ID,
    "rating": 5,
    "review": "Great book!",
    "is_active": True,
}


@pytest.fixture(autouse=True)
def mock_user():
    app.dependency_overrides[get_current_user] = lambda: {"id": USER_ID}
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def mock_review_service():
    svc = MagicMock()
    app.dependency_overrides[Provide[Container.review_service]] = lambda: svc
    app.container.review_service.override(providers.Object(svc))
    yield svc
    app.dependency_overrides.pop(Provide[Container.review_service], None)
    app.container.review_service.reset_override()


def test_create_review(mock_review_service: MagicMock):
    mock_review_service.add.return_value = MOCK_REVIEW
    payload = ReviewInCreate(
        user_id=UUID(USER_ID),
        book_id=UUID(BOOK_ID),
        rating=5,
        review="Great book!",
    )
    resp = client.post("/reviews/", json=payload.model_dump(mode="json"))
    assert resp.status_code == 201
    assert resp.json() == MOCK_REVIEW


def test_read_reviews(mock_review_service: MagicMock):
    mock_review_service.get_all.return_value = [MOCK_REVIEW]
    resp = client.get("/reviews/?offset=0&limit=10&filter=")
    assert resp.status_code == 200
    assert resp.json() == [MOCK_REVIEW]


def test_read_review(mock_review_service: MagicMock):
    mock_review_service.get_by_id.return_value = MOCK_REVIEW
    resp = client.get(f"/reviews/{REVIEW_ID}")
    assert resp.status_code == 200
    assert resp.json() == MOCK_REVIEW


def test_update_review(mock_review_service: MagicMock):
    update = ReviewInUpdate(
        rating=4,
        review="Still good",
        is_active=True,
    )
    expected = {**MOCK_REVIEW, **update.model_dump(exclude_unset=True)}
    mock_review_service.update.return_value = expected
    resp = client.put(
        f"/reviews/{REVIEW_ID}",
        json=update.model_dump(exclude_unset=True),
    )
    assert resp.status_code == 200
    assert resp.json() == expected


def test_delete_review(mock_review_service: MagicMock):
    mock_review_service.delete.return_value = None
    resp = client.delete(f"/reviews/{REVIEW_ID}")
    assert resp.status_code == 204
