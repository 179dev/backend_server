from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from server.database.db_settings import SessionLocal
from server.database.db_context import DBContext
from server.database.schemas.users import UserLogin, UserGet
from server.database.entities.users import User
from server.database.entities.users import hash_password
from datetime import datetime
from server.config import (
    TOKEN_EXPIRE_TIME,
    TOKEN_GENERATION_ALGORITHM,
    TOKEN_SECRET_KEY,
)
from jose import jwt
from server import main_repo

router = APIRouter()


def db_context():
    db = SessionLocal()
    try:
        yield DBContext(db)
    finally:
        db.close()


def generate_token(user: UserLogin, ctx: DBContext = Depends(db_context)):
    token_expiration_date = datetime.utcnow() + TOKEN_EXPIRE_TIME
    to_encode = {
        "username": user.username,
        "exp": token_expiration_date,
    }
    token = jwt.encode(
        to_encode, key=TOKEN_SECRET_KEY, algorithm=TOKEN_GENERATION_ALGORITHM
    )
    user.token = token
    user.token_expiration_date = token_expiration_date
    return main_repo.users.insert(ctx, UserLogin)


@router.post("/login/by_mail", response_model=UserGet)
def login_by_mail(user: UserLogin, ctx: DBContext = Depends(db_context)):
    db_user = main_repo.users.get_by_email(ctx, email=user.email)
    if db_user is None or db_user.hashed_password != hash_password(user.password):
        raise HTTPException(status_code=400, detail="Email or password is invalid")
    db_user = generate_token(user, ctx)
    return db_user


@router.post("/login/by_username", response_model=UserGet)
def login_by_username(user: UserLogin, ctx: DBContext = Depends(db_context)):
    db_user = main_repo.users.get_by_username(ctx, username=user.username)
    if db_user is None or db_user.hashed_password != hash_password(user.password):
        raise HTTPException(status_code=400, detail="Email or password is invalid")
    db_user = generate_token(user, ctx)
    return db_user
