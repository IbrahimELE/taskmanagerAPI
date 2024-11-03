from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from models.task import Task
from schemas.task import TaskCreate


def create_task(db: Session, task: TaskCreate, user_id: str):
    db_task = Task(
        title = task.title,
        content = task.content,
        deadline = task.deadline,
        priority = task.priority,
        status = task.status,
        user_id=user_id 
        )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, user_id: str):
    return db.query(Task).filter(Task.user_id == user_id).all()

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks_by_priority(db: Session, user_id: str):
    return db.query(Task).filter(Task.user_id == user_id).order_by(desc(Task.priority)).all()

def get_tasks_by_status(db: Session, user_id: str, status: str):
    return db.query(Task).filter(Task.user_id==user_id, Task.status == status).all()

def get_task_by_deadline(db: Session, user_id: str):
    return db.query(Task).filter(Task.user_id == user_id).order_by(asc(Task.deadline)).all()

def update_task(db: Session, task_id: int, task: TaskCreate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        for key, value in task.model_dump().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        return db_task
    return None

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return db_task
    return None