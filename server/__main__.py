import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.domains import users, conferences
from server.debug import conference_debug
from server.database.db_settings import Base, engine
from server.config import ALLOWED_ORIGINS, DEBUG
from contextlib import asynccontextmanager

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    conferences.conference_garbage_collect()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(conferences.router)
if DEBUG:
    app.include_router(conference_debug.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
