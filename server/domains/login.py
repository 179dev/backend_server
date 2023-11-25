from fastapi import APIRouter, Depends, HTTPException
from server.database.db_settings import SessionLocal
from server.database.db_context import DBContext
from server.database.schemas.users import UserLogin, UserAuth
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
from server.utils import is_email

router = APIRouter()


def db_context():
    db = SessionLocal()
    try:
        yield DBContext(db)
    finally:
        db.close()


def update_token_in_user(user: User, ctx: DBContext = Depends(db_context)):
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


@router.post("/login", response_model=UserAuth)
def login(user: UserLogin, ctx: DBContext = Depends(db_context)):
    login = user.login
    if is_email(login):
        db_user = main_repo.users.get_by_email(ctx, email=login)
    else:
        db_user = main_repo.users.get_by_username(ctx, username=login)
    if db_user is None or db_user.hashed_password != hash_password(user.password):
        raise HTTPException(status_code=400, detail="Login or password is invalid")
    db_user = update_token_in_user(db_user, ctx)
    return db_user
