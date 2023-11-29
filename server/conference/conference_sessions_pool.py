from uuid import UUID, uuid4
import datetime
from typing import overload

from server.conference.conference_session import ConferenceSession
from server.conference.exceptions import ConferenceNotFound
from server.vendor.repeat_every import repeat_every
from server.config import CONFERENCE_GC_RATE


class ConferenceSessionsPool:
    _conference_sessions: dict[UUID, ConferenceSession]

    def __init__(self) -> None:
        self._conference_sessions = {}

    def create_conference_session(self, id: UUID = None) -> ConferenceSession:
        if id is None:
            id = uuid4()

        self._conference_sessions[id] = ConferenceSession(id)

        return self._conference_sessions[id]

    @overload
    def get_conference_session(self, id: str) -> ConferenceSession:
        ...

    @overload
    def get_conference_session(self, id: UUID) -> ConferenceSession:
        ...

    def get_conference_session(self, id: UUID | str) -> ConferenceSession:
        if isinstance(id, str):
            id = UUID(id)
        if id not in self._conference_sessions:
            raise ConferenceNotFound(f"Conference with ID {id} does not exist")
        return self._conference_sessions[id]

    @overload
    def terminate_conference_session(self, id: str):
        ...

    @overload
    def terminate_conference_session(self, id: UUID):
        ...

    def terminate_conference_session(self, id: UUID | str):
        if isinstance(id, str):
            id = UUID(id)
        del self._conference_sessions[id]

    async def run_conference_expiration_cycle(self):
        @repeat_every(seconds=CONFERENCE_GC_RATE)
        def loop():
            for cid, conference in self._conference_sessions.items():
                timestamp = datetime.datetime.utcnow()
                if not conference.is_active(timestamp):
                    del self._conference_sessions[cid]

        await loop()
