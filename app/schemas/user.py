from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
from datetime import datetime


class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"

class UserCreate(BaseModel):
    name: str
    email_address: EmailStr
    password: str = Field(min_length=8)
    role: Role

class UserOut(BaseModel):
    email_address: EmailStr
    name: str
    role: Role

    class Config:
        from_attributes = True

class User(BaseModel):
    name: str
    email_address: EmailStr
    password: str
    role: Role