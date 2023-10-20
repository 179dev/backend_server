import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME") or "postgres"
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME") or "postgres"
POSTGRES_HOST = os.getenv("POSTGRES_HOST") or "localhost"
POSTGRES_PORT = os.getenv("POSTGRES_PORT") or "5432"
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") or "admin"

DB_URL = (
    f"postgresql://"
    f"{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}"
    f"/{POSTGRES_DB_NAME}"
)


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
