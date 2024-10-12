from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database import Base

class Role(str, PyEnum):
    admin = "admin"
    manager = "manager"
    employee = "employee"

class UserDB(Base):
    __tablename__ = "users"

    e_mail = Column(String, primary_key=True, unique=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)