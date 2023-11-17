from fastapi import APIRouter, Depends, HTTPException
from server.database.db_settings import SessionLocal
from server.database.db_context import DBContext
from server.database.schemas.users import UserLogin, UserGet
from server.database.entities.users import User
from server.database.entities.users import hash_password
from datetime import datetime
from server.config import (
    AUTH_TOKEN_EXPIRE_TIME,
    TOKEN_GENERATION_ALGORITHM,
    GENERATION_TOKEN_SECRET_KEY,
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


def generate_token(user: User, ctx: DBContext = Depends(db_context)):
    token_expiration_date = datetime.utcnow() + AUTH_TOKEN_EXPIRE_TIME
    to_encode = {
        "username": user.username,
        "exp": token_expiration_date,
    }
    token = jwt.encode(
        to_encode, key=GENERATION_TOKEN_SECRET_KEY, algorithm=TOKEN_GENERATION_ALGORITHM
    )
    user.token = token
    user.token_expiration_date = token_expiration_date
    return main_repo.users.update_data(ctx, user)


@router.post("/login/by_email", response_model=UserGet)
def login_by_mail(user: UserLogin, ctx: DBContext = Depends(db_context)):
    db_user = main_repo.users.get_by_email(ctx, email=user.email)
    if db_user is None or db_user.hashed_password != hash_password(user.password):
        raise HTTPException(status_code=400, detail="Email or password is invalid")
    db_user = generate_token(db_user, ctx)
    return db_user


@router.post("/login/by_username", response_model=UserGet)
def login_by_username(user: UserLogin, ctx: DBContext = Depends(db_context)):
    db_user = main_repo.users.get_by_username(ctx, username=user.username)
    if db_user is None or db_user.hashed_password != hash_password(user.password):
        raise HTTPException(status_code=400, detail="Email or password is invalid")
    db_user = generate_token(db_user, ctx)
    db_user = main_repo.users.get_by_username(ctx, username=user.username)
    return db_user
