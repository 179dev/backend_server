from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routers import users
from server.database.db_settings import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)

origins = [
    "http://0.0.0.0",
    "http://0.0.0.0:8080",
    "http://0.0.0.0:3000",
    "http://0.0.0.0:8000",
    "http://0.0.0.0:8179",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8179",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
