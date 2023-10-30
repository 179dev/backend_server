from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database.db_settings import SessionLocal
from server.database.db_context import DBContext
from server.database.schemas.users import UserLogin, UserGet
from server.database.entities.users import User
from server.database.entities.users import hash_password
from server import main_repo

router = APIRouter()


def db_context():
    db = SessionLocal()
    try:
        yield DBContext(db)
    finally:
        db.close()


@router.post("/login/by_mail", response_model=UserGet)
def login_by_mail(user: UserLogin, db: DBContext = Depends(db_context)):
    pass


@router.post("/login/by_username", response_model=UserGet)
def login_by_username(user: UserLogin, db: DBContext = Depends(db_context)):
    pass
