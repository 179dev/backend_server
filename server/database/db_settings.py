import os
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from server.config import *


if not (
    POSTGRES_DB_NAME
    and POSTGRES_USERNAME
    and POSTGRES_HOST
    and POSTGRES_PORT
    and POSTGRES_PASSWORD
):
    raise ValueError("Incomplete environment variables.")


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
