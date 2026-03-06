from fastapi.testclient import TestClient

from fast_notes.api.notes import get_notes_service
from fast_notes.main import app
from fast_notes.services.notes_service import NoteService
from tests.integration.test_db import TestingSessionLocal

# Setup the TestClient
client = TestClient(app)


# Dependency to override the get_db dependency in the main app
def override_get_notes_service():
    session = TestingSessionLocal()
    yield NoteService(session=session)


app.dependency_overrides[get_notes_service] = override_get_notes_service


def test_create_and_get_note():
    # Create a new note
    response = client.post("/api/v1/notes", json={"title": "Test Note", "content": "This is a test note."})
    assert response.status_code == 200
    created_note = response.json()
    assert created_note["title"] == "Test Note"
    assert created_note["content"] == "This is a test note."
    assert "id" in created_note

    # Fetch the same note
    get_response = client.get(f"/api/v1/notes/{created_note['id']}")
    assert get_response.status_code == 200
    fetched_note = get_response.json()
    assert fetched_note["id"] == created_note["id"]
    assert fetched_note["title"] == "Test Note"
    assert fetched_note["content"] == "This is a test note."