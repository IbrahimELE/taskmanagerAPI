from sqlalchemy import Column, String, Enum, Integer, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.database import Base
from datetime import datetime, timezone

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
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable = False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(timezone.utc), nullable=True)

    user = relationship("UserDB", back_populates="tasks")