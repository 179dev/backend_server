from uuid import UUID, uuid4
import datetime
from typing import overload

from server.conference.conference_session import ConferenceSession
from server.conference.conference_controller import ConferenceController
from server.conference.exceptions import ConferenceNotFound
from server.vendor.repeat_every import repeat_every
from server.conference.message_coding.base_message_coder import BaseMessageCoder
from server.config import CONFERENCE_GC_RATE


class ConferenceManager:
    _conferences: dict[UUID, ConferenceController]
    message_coding: BaseMessageCoder

    def __init__(self, message_coding: BaseMessageCoder) -> None:
        self._conferences = {}
        self.message_coding = message_coding

    def create_conference(self, id: UUID = None) -> ConferenceController:
        if id is None:
            id = uuid4()

        new_conference_session = ConferenceSession(id)
        conference_controller = ConferenceController(
            conference=new_conference_session, message_coding=self.message_coding
        )

        self._conferences[id] = conference_controller

        return conference_controller

    @overload
    def get_conference(self, id: str) -> ConferenceController:
        ...

    @overload
    def get_conference(self, id: UUID) -> ConferenceController:
        ...

    def get_conference(self, id: UUID | str) -> ConferenceController:
        if isinstance(id, str):
            id = UUID(id)
        if id not in self._conferences:
            raise ConferenceNotFound(f"Conference with ID {id} does not exist")
        return self._conferences[id]

    @overload
    def terminate_conference(self, id: str):
        ...

    @overload
    def terminate_conference(self, id: UUID):
        ...

    def terminate_conference(self, id: UUID | str):
        if isinstance(id, str):
            id = UUID(id)
        del self._conferences[id]

    async def run_conference_expiration_cycle(self):
        @repeat_every(seconds=CONFERENCE_GC_RATE)
        def loop():
            for cid, conference in self._conferences.items():
                timestamp = datetime.datetime.utcnow()
                if conference.should_be_terminated(timestamp):
                    del self._conferences[cid]

        await loop()
