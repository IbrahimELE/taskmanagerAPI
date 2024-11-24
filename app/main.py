import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from database import engine, Base
from routers import task, user

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(task.router)
app.include_router(user.router)
















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
    