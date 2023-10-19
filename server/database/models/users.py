from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship, mapped_column, Mapped
from uuid import UUID
from server.database.db_settings import Base
from server.database.models.entity_like import EntityLikeMixin
from server.database.entities.users import User as UserEntity


class User(Base, EntityLikeMixin):
    __tablename__ = "users"
    __common_fields_with_entity__ = (
        "id",
        "email",
        "hashed_password",
        "settings",
    )
    __entity__ = UserEntity

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    settings: Mapped[str] = mapped_column(String(1024))
