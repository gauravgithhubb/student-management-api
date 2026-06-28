from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, SessionLocal
from security import create_access_token, verify_token
from app.routers import students, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(students.router)
app.include_router(users.router)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Student Management API with Database is running"}

