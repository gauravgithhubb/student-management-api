from pydantic import BaseModel

class StudentBase(BaseModel):
    name: str
    branch: str
    year: int
    email: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True