from fastapi import FastAPI, Depends, HTTPException, status, Security, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from typing import List, Annotated
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from schemas.user import UserCreate, UserOut
from schemas.token import Token
from crud.user import create_user, get_user_by_email
from app.utils.auth import  create_access_token, verify_password

router = APIRouter()
@router.post("/register/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email_address):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already in use",
        )

    return create_user(db, user)

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):

    user = get_user_by_email(db, form_data.username)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"Authorization": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email_address})
    return {"access_token": access_token, "token_type": "Bearer"}

@router.get("/users/{email_address}", response_model=UserOut)
def read_user(email_address: EmailStr, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email_address)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user




