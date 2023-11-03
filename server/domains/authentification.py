from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from server.database.db_settings import SessionLocal
from server.database.db_context import DBContext
from server.database.schemas.users import UserAuth
from server.database.entities.users import User
from server.database.entities.users import hash_password
from server import main_repo


def db_context():
    db = SessionLocal()
    try:
        yield DBContext(db)
    finally:
        db.close()


def authenticate_user(user: UserAuth, db: DBContext = Depends(db_context)):
    db_user = main_repo.users.get_by_token(db, user.token)
    if not db_user:
        raise HTTPException(status_code=401, detail="Authorization error")
    return db_user
