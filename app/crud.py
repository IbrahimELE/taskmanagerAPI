from sqlalchemy.orm import Session
from app.models import UserDB
from app.schemas import UserCreate
import bcrypt

def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = UserDB(
        e_mail=user.e_mail,
        name=user.name,
        password=hashed_password.decode("utf-8"),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, e_mail: str):
    return db.query(UserDB).filter(UserDB.e_mail == e_mail).first()