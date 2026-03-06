from sqlalchemy.orm import Session

from fast_notes.db.schema import Note


class NoteService:
    def __init__(self, session: Session):
        self._db = session

    def list_notes(self):
        return self._db.query(Note).all()

    def get_note(self, note_id: int):
        return self._db.query(Note).filter(Note.id == note_id).first()

    def create_note(self, title: str, content: str):
        note = Note(title=title, content=content)
        self._db.add(note)
        self._db.commit()
        self._db.refresh(note)
        return note

    def update_note(self, note_id: int, title: str, content: str):
        note = self.get_note(note_id)
        if not note:
            return None

        note.title = title
        note.content = content
        self._db.commit()
        self._db.refresh(note)
        return note

    def delete_note(self, note_id: int):
        note = self.get_note(note_id)
        if not note:
            return False

        self._db.delete(note)
        self._db.commit()
        return True
