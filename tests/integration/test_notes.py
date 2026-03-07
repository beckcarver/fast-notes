from fastapi.testclient import TestClient
from pytest import fixture

from fast_notes.api.notes import get_notes_service
from fast_notes.main import app
from fast_notes.services.notes_service import NoteService
from tests.integration.test_db import TestingSessionLocal


# Dependency to override the get_db dependency in the main app
def override_get_notes_service():
    session = TestingSessionLocal()
    yield NoteService(session=session)


@fixture
def client():
    # Create and populate the test database
    client = TestClient(app)
    app.dependency_overrides[get_notes_service] = override_get_notes_service
    return client


def test_get_notes_empty(client):
    res = client.get("/api/v1/notes")
    assert res.status_code == 200
    assert res.json() == []


def test_get_nonexistent_note(client):
    res = client.get("/api/v1/notes/999")
    assert res.status_code == 404
    assert res.json() == {"detail": "Note not found"}


def test_create_note(client):
    res = client.post(
        "/api/v1/notes", json={"title": "Test Note", "content": "Lebron james"}
    )
    assert res.status_code == 200
    created_note = res.json()
    assert created_note["title"] == "Test Note"
    assert created_note["content"] == "Lebron james"
    assert "id" in created_note


def test_create_and_get_note(client):
    # Create a new note
    res = client.post(
        "/api/v1/notes", json={"title": "Test Note", "content": "Lebron james"}
    )
    assert res.status_code == 200
    created_note = res.json()
    assert created_note["title"] == "Test Note"
    assert created_note["content"] == "Lebron james"
    assert "id" in created_note

    # Fetch the same note
    get_res = client.get(f"/api/v1/notes/{created_note['id']}")
    assert get_res.status_code == 200
    fetched_note = get_res.json()
    assert fetched_note["id"] == created_note["id"]
    assert fetched_note["title"] == "Test Note"
    assert fetched_note["content"] == "Lebron james"


def test_create_and_update_note(client):
    # create a new note
    res = client.post(
        "/api/v1/notes", json={"title": "Test Note", "content": "Lebron james"}
    )
    assert res.status_code == 200
    created_note = res.json()
    assert created_note["title"] == "Test Note"
    assert created_note["content"] == "Lebron james"
    assert "id" in created_note

    # update the note
    update_res = client.put(
        f"/api/v1/notes/{created_note['id']}",
        json={"title": "Updated Note", "content": "Bronny james."},
    )
    assert update_res.status_code == 200
    updated_note = update_res.json()
    assert updated_note["id"] == created_note["id"]
    assert updated_note["title"] == "Updated Note"
    assert updated_note["content"] == "Bronny james."


def test_create_and_delete_note(client):
    # create a new note
    res = client.post(
        "/api/v1/notes", json={"title": "Test Note", "content": "Lebron james"}
    )
    assert res.status_code == 200
    created_note = res.json()
    assert created_note["title"] == "Test Note"
    assert created_note["content"] == "Lebron james"
    assert "id" in created_note

    # delete the note
    delete_res = client.delete(f"/api/v1/notes/{created_note['id']}")
    assert delete_res.status_code == 200
    assert delete_res.json() == {
        "detail": f"Note {created_note['id']} deleted successfully"
    }

    # try to fetch the deleted note
    get_res = client.get(f"/api/v1/notes/{created_note['id']}")
    assert get_res.status_code == 404


def create_notes_get_all_notes(client):
    # create multiple notes
    for i in range(10):
        res = client.post(
            "/api/v1/notes", json={"title": f"Note {i}", "content": f"Content {i}"}
        )
        assert res.status_code == 200

    # fetch all notes
    get_res = client.get("/api/v1/notes")
    assert get_res.status_code == 200
    notes = get_res.json()
    assert (
        len(notes) >= 10
    )  # there may be more notes from other tests, but at least 10 should be present
    for i in range(10):
        assert any(
            note["title"] == f"Note {i}" and note["content"] == f"Content {i}"
            for note in notes
        )
