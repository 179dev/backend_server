from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from uuid import UUID
from server.database.db_settings import Base
from server.database.models.entity_like import EntityLikeMixin
from server.database.entities.users import User as UserEntity
import json


class User(Base, EntityLikeMixin):
    __tablename__ = "users"
    __common_fields_with_entity__ = (
        "id",
        "email",
        "hashed_password",
        "username",
        "display_name",
        "token",
        "token_expiration_date",
    )

    __entity__ = UserEntity
    __attrs_from_entity__ = {"settings": json.dumps}
    __attrs_to_entity__ = {"settings": json.loads}

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(256), unique=True)
    display_name: Mapped[str] = mapped_column(String(256), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String)
    settings: Mapped[str] = mapped_column(String(1024), default="{}")
    token: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    token_expiration_date: Mapped[DateTime] = mapped_column(DateTime)
