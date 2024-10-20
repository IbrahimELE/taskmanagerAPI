from sqlalchemy.orm import Session
from models import UserDB, Task
from schemas import UserCreate, TaskCreate
import bcrypt

def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = UserDB(
        email_address=user.email_address,
        name=user.name,
        password=hashed_password.decode("utf-8"),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email_address: str):
    return db.query(UserDB).filter(UserDB.email_address == email_address).first()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_task(db: Session, task: TaskCreate, user_id: str):
    db_task = Task(**task.model_dump(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, user_id: str):
    return db.query(Task).filter(Task.user_id == user_id).all()

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

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