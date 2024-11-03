from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
from datetime import datetime, timezone

from typing import Optional

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"

class TaskCreate(BaseModel):
    title: str
    content: str
    deadline: datetime
    priority: int = 1  
    status: TaskStatus = TaskStatus.pending


    model_config = ConfigDict(arbitrary_types_allowed=True)

class TaskOut(BaseModel):
    id: int
    title: str
    content: str
    deadline: datetime
    priority: int
    status: TaskStatus
    user_id: str  
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True 