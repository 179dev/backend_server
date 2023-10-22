import os

INNER_PORT = os.getenv("INNER_PORT")

if not INNER_PORT:
    raise ValueError("Incomplete environment variables.")

ALLOWED_ORIGINS = [
    "http://0.0.0.0",
    "http://0.0.0.0:8000",
    f"http://0.0.0.0:{INNER_PORT}",
    "http://localhost",
    "http://localhost:8000",
    f"http://localhost:{INNER_PORT}",
]
