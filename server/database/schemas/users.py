from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    """Common user data shared by all schemas"""

    email: str | None = None
    username: str | None = None


class UserGet(UserBase):
    """User data which can be read"""

    id: UUID
    display_name: str | None = None


class UserCreate(UserBase):
    """User data which can be written"""

    password: str
    display_name: str | None = None

    class Config:
        orm_mode = True


class UserAuth(UserBase):
    """User data for authentication"""

    token: str
    token_expiration_date: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    """User data for logging in"""

    login: str = Field(
        title="User's login string",
        description=(
            "This could be either a username or an email."
            " The server will automatically detect the type of given data based on it's format"
        ),
        examples=["john_doe_cool_username", "john_doe@email.com"],
    )
    password: str
