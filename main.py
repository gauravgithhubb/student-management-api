from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, SessionLocal
from security import create_access_token, verify_token
from app.routers import students

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(students.router)

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

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.login_user(db, user)

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": db_user.email})

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

@app.get("/me", response_model=schemas.UserResponse)
def get_current_user(
    current_user_email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, current_user_email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user