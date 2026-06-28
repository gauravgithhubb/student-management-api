import auth

from sqlalchemy.orm import Session
import models
import schemas

def create_student(db: Session, student: schemas.StudentCreate):
    new_student = models.Student(
        name=student.name,
        branch=student.branch,
        year=student.year,
        email=student.email
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def get_students(db: Session):
    return db.query(models.Student).all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def delete_student(db: Session, student_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if student:
        db.delete(student)
        db.commit()

    return student

def update_student(db: Session, student_id: int, updated_student: schemas.StudentCreate):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if student is None:
        return None

    student.name = updated_student.name
    student.branch = updated_student.branch
    student.year = updated_student.year
    student.email = updated_student.email

    db.commit()
    db.refresh(student)

    return student

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(db: Session, user: schemas.UserLogin):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if db_user is None:
        return None

    if not auth.verify_password(user.password, db_user.password):
        return None

    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()