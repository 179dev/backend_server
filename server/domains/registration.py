from fastapi import APIRouter, Depends, HTTPException

from server.database.db_settings import SessionLocal
from server.database.db_context import DBContext
from server.database.schemas.users import UserCreate, UserGet
from server.database.entities.users import User
from server import main_repo
from server.utils import is_email

router = APIRouter()


def db_context():
    db = SessionLocal()
    try:
        yield DBContext(db)
    finally:
        db.close()


@router.post("/register/", response_model=UserGet)
def create_user(user: UserCreate, db: DBContext = Depends(db_context)):
    db_user = main_repo.users.find_user(db, email=user.email, username=user.username)
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already registered")
        elif db_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(
                status_code=400,
                detail=f"User already exists",
            )
    if not is_email(user.email):
        raise HTTPException(status_code=400, detail="Email not accessable")
    new_user = User.create(user)
    return main_repo.users.insert(db, new_user)
