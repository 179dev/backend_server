from sqlalchemy.orm import Session
from uuid import UUID, uuid4
import dataclasses
from server.database.schemas.users import UserCreate


@dataclasses.dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    username: str
    display_name: str | None = None 
    settings: str = dataclasses.field(default_factory=dict)

    @classmethod
    def create(cls, user: UserCreate):
        hashed_password = user.password + "debug_not_really_hashed"  # FIXME

        new_user = cls(
            id=uuid4(),
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            settings={},
        )
        return new_user
