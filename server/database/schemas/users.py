from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    """Common user data shared by all schemas"""

    email: str
    username: str


class UserGet(UserBase):
    """User data which can be read"""

    id: UUID
    display_name: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    """User data which can be written"""

    password: str
    displayname: str

    class Config:
        orm_mode = True


class UserAuth(UserBase):
    """User data for authentification"""

    token: str

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    """User data for logging in"""

    login: str
    password: str

    class Config:
        orm_mode = True
