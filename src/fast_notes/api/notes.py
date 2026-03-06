from fastapi import APIRouter, Depends, HTTPException

from fast_notes.db.schema import SessionLocal
from fast_notes.models.note import NoteCreate, NoteRead
from fast_notes.services.notes_service import NoteService

router = APIRouter()


def get_notes_service():
    return NoteService(session=SessionLocal())


@router.get("/notes", response_model=list[NoteRead])
def get_notes(service: NoteService = Depends(get_notes_service)):
    return service.list_notes()


@router.get("/notes/{note_id}", response_model=NoteRead)
def get_note(note_id: int, service: NoteService = Depends(get_notes_service)):
    note = service.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("/notes", response_model=NoteRead)
def create_note(note: NoteCreate, service: NoteService = Depends(get_notes_service)):
    return service.create_note(title=note.title, content=note.content)


@router.put("/notes/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int, note: NoteCreate, service: NoteService = Depends(get_notes_service)
):
    updated_note = service.update_note(
        note_id=note_id, title=note.title, content=note.content
    )
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note


@router.delete("/notes/{note_id}")
def delete_note(note_id: int, service: NoteService = Depends(get_notes_service)):
    success = service.delete_note(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"success": True}
