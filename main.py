from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Student Management API with Database is running"}

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

from security import create_access_token, verify_token

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.login_user(db, user)

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/profile")
def get_profile(current_user_email: str = Depends(verify_token)):
    return {
        "message": "Profile accessed successfully",
        "user_email": current_user_email
    }

@app.post("/students", response_model=schemas.StudentResponse)
def add_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@app.get("/students", response_model=list[schemas.StudentResponse])
def view_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def view_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student

@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def edit_student(student_id: int, updated_student: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = crud.update_student(db, student_id, updated_student)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student

@app.delete("/students/{student_id}")
def remove_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.delete_student(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}