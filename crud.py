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