import os
import datetime

# Env variables
INNER_PORT = os.getenv("INNER_PORT")
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DEBUG = os.getenv("DEBUG") != "false"

# Conference garbage collection constants:
CONFERENCE_EXPIRATION_TIME = (
    datetime.timedelta(hours=2) if not DEBUG else datetime.timedelta(minutes=10)
)  # NOTE: In debug mode unused or inactive conferences have TTL if 10 minutes.
CONFERENCE_GC_RATE = 60 * 60 if not DEBUG else 60
# NOTE: In debug mode garbage collection is performed every minute.

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
