from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, UserDB
from app.schemas import UserCreate, UserOut
from app.crud import create_user, get_user_by_email

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.e_mail)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user(db=db, user=user)

@app.get("/users/{e_mail}", response_model=UserOut)
def read_user(e_mail: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, e_mail)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

























# from fastapi import FastAPI
# from pydantic import BaseModel, EmailStr, field_validator, Field
# import datetime
# from typing import Optional, Literal
# from enum import Enum
# app = FastAPI()

# @app.get("/")
# def root():
#     return {"message": "ide ovo"}

# class Role(str, Enum):
#     admin = "admin"
#     manager = "manager"
#     employee = "employee"

# class Task_Details(BaseModel):
#     deadline: datetime
#     priority: int = Field(default=1, ge=1, le=10)
#     status: Literal["pending", "in-progress", "completed"]

# class Task(BaseModel):
#     title: str
#     content: str
#     details: Task_Details

# class User(BaseModel):
#     name: str
#     e_mail: EmailStr
#     password: str = Field(min_value=8)
#     role: Role

#     @field_validator('name')
#     def name_must_not_be_empty(cls, v):
#         if not v.strip():
#             raise ValueError('Name cannot be empty or whitespace only')
#         return v

#     @classmethod
#     def register(cls, name: str, e_mail: str, password: str, role: Role):
#         """Simulates user registration."""
#         return cls(name=name, e_mail=e_mail, password=password, role=role)
    