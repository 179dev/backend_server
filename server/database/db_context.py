from sqlalchemy.orm import Session


class DBContext:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    @property
    def session(self):
        return self._session
