from server.conference.conference_manager import ConferenceManager
from server.conference.message_coding.json_message_coder import JSONMessageCoder
from server.config import CONFERENCE_MESSAGE_CONTRACT

match CONFERENCE_MESSAGE_CONTRACT:
    case "json":
        main_message_coding = JSONMessageCoder()
    case _:
        main_message_coding = JSONMessageCoder()

main_conference_manager = ConferenceManager(message_coding=main_message_coding)
