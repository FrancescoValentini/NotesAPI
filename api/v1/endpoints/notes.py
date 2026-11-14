import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
from models import User
from schemas import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    APIResponse
)
from services import note_service
from api.v1.dependencies import get_current_user


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/",response_model=APIResponse[NoteResponse],status_code=status.HTTP_201_CREATED)
def create_note(data: NoteCreate,db: Session = Depends(get_db),user: User = Depends(get_current_user)):
    note = note_service.create_note(db, user.id, data)

    return APIResponse(
        result=note,
        message="Note created successfully"
    )


@router.get("/",response_model=APIResponse[list[NoteResponse]])
def get_notes(db: Session = Depends(get_db),user: User = Depends(get_current_user)):
    notes = note_service.get_notes(db, user.id)

    return APIResponse(
        result=notes,
        message="Notes retrieved successfully"
    )


@router.get("/{note_id}",response_model=APIResponse[NoteResponse])
def get_note(note_id: uuid.UUID,db: Session = Depends(get_db),user: User = Depends(get_current_user)):
    note = note_service.get_note(db, note_id, user.id)

    if not note:
        raise HTTPException(404, detail="Note not found")

    return APIResponse(result=note)


@router.put("/{note_id}",response_model=APIResponse[NoteResponse])
def update_note(note_id: uuid.UUID,data: NoteUpdate,db: Session = Depends(get_db),user: User = Depends(get_current_user)):
    note = note_service.get_note(db, note_id, user.id)

    if not note:
        raise HTTPException(404, detail="Note not found")

    updated_note = note_service.update_note(db, note, data)

    return APIResponse(
        result=updated_note,
        message="Note updated successfully"
    )


@router.delete("/{note_id}",response_model=APIResponse[None])
def delete_note(note_id: uuid.UUID,db: Session = Depends(get_db),user: User = Depends(get_current_user)):
    note = note_service.get_note(db, note_id, user.id)

    if not note:
        raise HTTPException(404, detail="Note not found")

    note_service.delete_note(db, note)

    return APIResponse(
        result=None,
        message="Note deleted successfully"
    )