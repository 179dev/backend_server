from uuid import UUID

from server.database.repo.base_repo_module import BaseRepoModule
from server.database.models import users as users_models
from server.database.schemas import users as users_schemas
from server.database.entities import users as users_entities
from server.database.db_context import DBContext
from server.database.repo.exceptions import InvalidRepoCall
from sqlalchemy import update, false, or_


class UserRepoModule(BaseRepoModule):
    def get_by_id(self, ctx: DBContext, user_id: UUID) -> users_models.User:
        user = (
            ctx.session.query(users_models.User)
            .filter(users_models.User.id == user_id)
            .first()
        )
        return user and user.as_entity()

    def get_by_email(self, ctx: DBContext, email: str) -> users_models.User:
        user = (
            ctx.session.query(users_models.User)
            .filter(users_models.User.email == email)
            .first()
        )
        return user and user.as_entity()

    def get_by_username(self, ctx: DBContext, username: str) -> users_models.User:
        user = (
            ctx.session.query(users_models.User)
            .filter(users_models.User.username == username)
            .first()
        )
        return user and user.as_entity()

    def get_by_token(self, ctx: DBContext, token: str) -> users_models.User:
        user = (
            ctx.session.query(users_models.User)
            .filter(users_models.User.token == token)
            .first()
        )
        return user

    def find_user(
        self,
        ctx: DBContext,
        email: str = None,
        username: str = None,
        id: UUID = None,
        token: str = None,
    ):
        """
        Returns a user which matches either of given criteria.
        Note that the criteria are disjuncted here, not conjuncted.
        Do not use with one criteria! Use a getter method for a specific field instead.
        """
        if not (email or username or id or token):
            raise InvalidRepoCall(
                "Neither email, nor username, nor id, not token are specified"
            )

        column_checks = []
        if email:
            column_checks.append(users_models.User.email == email)
        if username:
            column_checks.append(users_models.User.username == username)
        if id:
            column_checks.append(users_models.User.id == id)
        if token:
            column_checks.append(users_models.User.token == token)

        criteria = or_(false(), *column_checks)

        user = ctx.session.query(users_models.User).filter(criteria).first()
        return user

    def every(self, ctx: DBContext, skip: int = 0, limit: int = 100):
        return map(
            users_models.User.as_entity,
            ctx.session.query(users_models.User).offset(skip).limit(limit).all(),
        )

    def update_data(self, ctx: DBContext, user: users_entities.User):
        """
        Function for updating data in database.
        """
        model = users_models.User.from_entity(user)
        ctx.session.merge(model)
        ctx.session.commit()
        return self.get_by_id(ctx, model.id)

    def insert(self, ctx: DBContext, user: users_entities.User):
        db_user = users_models.User.from_entity(user)
        ctx.session.add(db_user)
        ctx.session.commit()
        ctx.session.refresh(db_user)
        return user
