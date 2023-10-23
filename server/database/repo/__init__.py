from server.database.repo.users import UserRepoModule


class Repo:
    users: UserRepoModule

    def __init__(self) -> None:
        self.users = UserRepoModule()
