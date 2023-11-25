import os
from datetime import timedelta
import email_validator

INNER_PORT = os.getenv("INNER_PORT")
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
GENERATION_TOKEN_SECRET_KEY = os.getenv("GENERATION_TOKEN_SECRET_KEY")
TOKEN_GENERATION_ALGORITHM = os.getenv("TOKEN_GENERATION_ALGORITHM")
AUTH_TOKEN_EXPIRE_TIME = timedelta(days=42)
DEBUG = os.getenv("DEBUG") == "true"

if DEBUG:
    email_validator.CHECK_DELIVERABILITY = False

if not (
    POSTGRES_DB_NAME
    and POSTGRES_USERNAME
    and POSTGRES_HOST
    and POSTGRES_PORT
    and POSTGRES_PASSWORD
    and INNER_PORT
):
    raise ValueError("Incomplete environment variables.")

ALLOWED_ORIGINS = [
    "http://0.0.0.0",
    "http://0.0.0.0:8000",
    f"http://0.0.0.0:{INNER_PORT}",
    "http://localhost",
    "http://localhost:8000",
    f"http://localhost:{INNER_PORT}",
]
