from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import auth

router = APIRouter(prefix = "/notes", tags = ["notes"])

@router.post("/", response_model = schemas.NoteResponse, status_code = 201)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    new_note = models.Note(
        title = note.title,
        content = note.content,
        is_published = note.is_published,
        owner_id = current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.get("/{note_id}", response_model = schemas.NoteResponse)
def get_note(
    note_id: int,   # Taken from URL path
    current_user = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    note  = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code = 404, detail = "Note not found.")
    return note

@router.put("/{note_id}", response_model = schemas.NoteUpdate)
def update_note(
    note_id: int,
    updated: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    note  = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code = 404, detail ="Note not found.")
    
    # Only update fields that where actually sent
    if updated.title is not None:
        note.title = updated.title
    if updated.content is not None:
        note.content = updated.content
    if updated.is_published is not None:
        note.is_published = updated.is_published
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}", status_code = 204)
def delete_note(
    note_id: int,
    current_user = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.owner_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code = 404, detail = "Note not found.")
    db.delete(note)
    db.commit()

@router.get("/", response_model = list[schemas.NoteResponse])
def list_notes(
    current_user = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    current_user_notes = db.query(models.Note).filter(models.Note.owner_id == current_user.id).all()
    return current_user_notes
