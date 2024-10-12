from pydantic import BaseModel, EmailStr, Field
from enum import Enum as PyEnum

class Role(str, PyEnum):
    admin = "admin"
    manager = "manager"
    employee = "employee"

class UserCreate(BaseModel):
    name: str
    e_mail: EmailStr
    password: str = Field(min_length=8)
    role: Role

class UserOut(BaseModel):
    e_mail: EmailStr
    name: str
    role: Role

    class Config:
        orm_mode = True 