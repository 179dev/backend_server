from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.domains import users
from server.domains import login
from server.domains import registration
from server.database.db_settings import Base, engine
from server.config import ALLOWED_ORIGINS

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router, login.router, registration.router)


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
