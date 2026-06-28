from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from security import create_access_token, verify_token

router = APIRouter(
    tags=["Users"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.post("/login")
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


@router.get("/profile")
def get_profile(current_user_email: str = Depends(verify_token)):
    return {
        "message": "Profile accessed successfully",
        "user_email": current_user_email
    }


@router.get("/me", response_model=schemas.UserResponse)
def get_current_user(
    current_user_email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, current_user_email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user