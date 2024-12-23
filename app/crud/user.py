from sqlalchemy.orm import Session
from models.user import UserDB
from schemas.user import UserCreate
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


