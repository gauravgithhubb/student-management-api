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

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str