import datetime

from server.conference.conference import Conference
from server.conference.conference_controller import ConferenceController
from server.conference.exceptions import ConferenceNotFound
from server.vendor.repeat_every import repeat_every
from server.conference.message_coding.base_message_coder import BaseMessageCoder
from server.config import CONFERENCE_GC_RATE
from server.conference.types import ConferenceID


class ConferencesPool:
    _conferences: dict[ConferenceID, ConferenceController]
    message_coding: BaseMessageCoder

    def __init__(self, message_coding: BaseMessageCoder) -> None:
        self._conferences = {}
        self.message_coding = message_coding

    def create_conference(self, id: ConferenceID = None) -> ConferenceController:
        if id is None:
            id = ConferenceID()

        new_conference = Conference(id)
        conference_controller = ConferenceController(
            conference=new_conference, message_coding=self.message_coding
        )

        self._conferences[id] = conference_controller

        return conference_controller

    def get_conference(self, id: ConferenceID) -> ConferenceController:
        try:
            return self._conferences[id]
        except KeyError:
            raise ConferenceNotFound("Conference {id} does not exist")

    def terminate_conference(self, id: ConferenceID):
        del self._conferences[id]

    async def run_conference_expiration_cycle(self):
        @repeat_every(seconds=CONFERENCE_GC_RATE)
        def loop():
            for cid, conference in self._conferences.items():
                timestamp = datetime.datetime.utcnow()
                if conference.should_be_terminated(timestamp):
                    del self._conferences[cid]

        await loop()
