from pydantic import BaseModel, EmailStr, Field

class StudentBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    branch: str = Field(..., min_length=2, max_length=50)
    year: int = Field(..., ge=1, le=4)
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True