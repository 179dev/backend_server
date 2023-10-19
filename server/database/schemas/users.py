from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    """Common user data shared by all schemas"""

    email: str
    settings: str


class UserGet(UserBase):
    """User data which can be read"""

    id: UUID

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    """User data which can be written"""

    password: str
