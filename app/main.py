import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from typing import List
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models.user import UserDB
from schemas.user import UserCreate, UserOut
from schemas.task import TaskCreate, TaskOut
from crud.user import create_user, get_user_by_email, verify_password
from crud.task import create_task, get_tasks, get_task
from app.utils.auth import get_password_hash, get_current_user, create_access_token, verify_password
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email_address):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already in use",
        )
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    return create_user(db, user)

@app.get("/users/{email_address}", response_model=UserOut)
def read_user(email_address: EmailStr, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email_address)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@app.post("/token/")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"Authorization": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email_address})
    return {"access_token": access_token, "token_type": "Bearer"}

@app.post("/tasks/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db), user: UserOut = Depends(get_current_user)):
    return create_task(db=db, task=task, user_id=user.email_address)

@app.get("/tasks/", response_model=List[TaskOut])
def read_tasks(db: Session = Depends(get_db), user: UserOut = Depends(get_current_user)):
    return get_tasks(db=db, user_id=user.email_address)

@app.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    updated_task = update_task(db=db, task_id=task_id, task=task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}", response_model=TaskOut)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = delete_task(db=db, task_id=task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task



















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
    