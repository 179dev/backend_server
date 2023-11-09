import os
from dotenv import load_dotenv

load_dotenv()

INNER_PORT = os.getenv("INNER_PORT")
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

DB_URL = (
    f"postgresql://"
    f"{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}"
    f"/{POSTGRES_DB_NAME}"
)
