from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database.db_settings import SessionLocal
from server.database.db_context import DBContext
from server.database.schemas.users import UserCreate, UserGet
from server.database.entities.users import User
from server import main_repo

router = APIRouter()


def db_context():
    db = SessionLocal()
    try:
        yield DBContext(db)
    finally:
        db.close()


@router.post("/users/", response_model=UserGet)
def create_user(user: UserCreate, db: DBContext = Depends(db_context)):
    db_user = main_repo.users.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User.create(user)
    return main_repo.users.insert(db, new_user)


@router.get("/users/", response_model=list[UserGet])
def read_users(
    skip: int = 0, limit: int = 100, ctx: DBContext = Depends(db_context)
):
    return list(main_repo.users.every(ctx, skip=skip, limit=limit))


@router.get("/users/{user_id}", response_model=UserGet)
def read_user(user_id: int, ctx: DBContext = Depends(db_context)):
    db_user = main_repo.users.get_by_id(ctx, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
