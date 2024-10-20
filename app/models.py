from sqlalchemy import Column, String, Enum, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from database import Base
class Role(str, PyEnum):
    admin = "admin"
    manager = "manager"
    employee = "employee"

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email_address = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)

    tasks = relationship("Task", back_populates="user") 
class TaskStatus(str, PyEnum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)
    priority = Column(Integer, default=1)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    user_id = Column(String, ForeignKey("users.email_address"))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user = relationship("UserDB", back_populates="tasks")