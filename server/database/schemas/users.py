from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    """Common user data shared by all schemas"""

    email: str
    username: str


class UserGet(UserBase):
    """User data which can be read"""

    id: UUID
    display_name: str | None


class UserCreate(UserBase):
    """User data which can be written"""

    password: str

    class Config:
        orm_mode = True
