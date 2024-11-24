from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import EmailStr
from typing import List
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from schemas.user import UserOut
from schemas.task import TaskCreate, TaskOut, TaskStatus
from crud.task import create_task, get_tasks, get_task, update_task, delete_task, get_tasks_by_priority, get_tasks_by_status, get_task_by_deadline
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/tasks/", response_model=TaskOut)
def task_maker(task: TaskCreate, db: Session = Depends(get_db), user: UserOut = Depends(get_current_user)):
    return create_task(db, task, user.email_address)

@router.get("/tasks/", response_model=List[TaskOut])
def read_tasks(db: Session = Depends(get_db), user: UserOut = Depends(get_current_user)):
    return get_tasks(db=db, user_id=user.email_address)

@router.get("/tasks/priority_first/", response_model=List[TaskOut]) 
def filter_tasks_by_priority(db: Session = Depends(get_db), user: UserOut = Depends(get_current_user)):
    return get_tasks_by_priority(db=db, user_id=user.email_address)

@router.get("/tasks/status_choose/{status}", response_model=List[TaskOut])
def filter_tasks_by_status(status: TaskStatus, db: Session = Depends(get_db), user: UserOut = Depends(get_current_user)):
    return get_tasks_by_status(db=db, user_id=user.email_address, status=status)

@router.get("/tasks/deadline_first", response_model=List[TaskOut])
def filter_tasks_by_deadline(db: Session = Depends(get_db), user: UserOut = Depends(get_current_user)):
    return get_task_by_deadline(db=db, user_id=user.email_address)

@router.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db), user: UserOut = Depends(get_current_user)):
    try:
        task = get_task(db=db, task_id=task_id, user_id=user.email_address)
        return task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.put("/tasks/{task_id}", response_model=TaskOut)
def full_update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    
    updated_task = update_task(db=db, task_id=task_id, task=task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}", response_model=TaskOut)
def delete_selected_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = delete_task(db=db, task_id=task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task