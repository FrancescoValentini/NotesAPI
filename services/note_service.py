import uuid

from sqlalchemy.orm import Session

from models import Note
from schemas import NoteCreate, NoteUpdate


def create_note(db: Session,user_id: uuid.UUID,data: NoteCreate) -> Note:
    note = Note(title=data.title,content=data.content,user_id=user_id)

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


def get_notes(db: Session,user_id: uuid.UUID) -> list[Note]:
    return db.query(Note).filter(Note.user_id == user_id).all()


def get_note(db: Session,note_id: uuid.UUID,user_id: uuid.UUID) -> Note | None:
    return db.query(Note).filter(Note.id == note_id,Note.user_id == user_id).first()


def update_note(db: Session,note: Note,data: NoteUpdate) -> Note:
    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)

    return note


def delete_note(db: Session, note: Note) -> None:
    db.delete(note)
    db.commit()