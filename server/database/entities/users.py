from sqlalchemy.orm import Session
from uuid import UUID, uuid4
import dataclasses
from datetime import datetime
from server.database.schemas.users import UserCreate


def hash_password(password: str):
    return password + "debug_not_really_hashed"  # FIXME


@dataclasses.dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    username: str
    display_name: str = None
    settings: str = dataclasses.field(default_factory=dict)
    token: str | None,
    token_expiration_date: datetime | None

    @classmethod
    def create(cls, user: UserCreate):
        hashed_password = hash_password(user.password)

        new_user = cls(
            id=uuid4(),
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            settings={},
            token=None,
            toxen_expire_date=None
        )
        return new_user
