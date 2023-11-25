from fastapi import HTTPException

from server.database.db_context import DBContext
from server.database.schemas.users import UserAuth
from server import main_repo
from datetime import datetime


def authenticate_user_from_token(token: str, db: DBContext):
    db_user = main_repo.users.get_by_token(db, token)
    if not db_user or db_user.token_expiration_date < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Authorization error")
    return db_user
