from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.StudentResponse)
def add_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_student(db, student)

@router.get("", response_model=list[schemas.StudentResponse])
def view_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@router.get("/{student_id}", response_model=schemas.StudentResponse)
def view_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@router.put("/{student_id}", response_model=schemas.StudentResponse)
def edit_student(
    student_id: int,
    updated_student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    student = crud.update_student(
        db,
        student_id,
        updated_student
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@router.delete("/{student_id}")
def remove_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.delete_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully"
    }