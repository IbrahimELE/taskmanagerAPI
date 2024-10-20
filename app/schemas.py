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

    class Config:
        from_attributes = True 