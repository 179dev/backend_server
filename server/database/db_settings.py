import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

if not (
    POSTGRES_DB_NAME
    and POSTGRES_USERNAME
    and POSTGRES_HOST
    and POSTGRES_PORT
    and POSTGRES_PASSWORD
):
    raise ValueError("Incomplete environment variables.")

DB_URL = (
    f"postgresql://"
    f"{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}"
    f"/{POSTGRES_DB_NAME}"
)


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
