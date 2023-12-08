from server.conference.conferences_pool import ConferencesPool
from server.conference.message_coding.json_message_coder import JSONMessageCoder
from server.config import (
    CONFERENCE_GC_RATE,
    CONFERENCE_EXPIRATION_TIME,
    CONFERENCE_SYNC_MEMBER_AND_CANVAS_IDS,
)


main_message_coding = JSONMessageCoder()

main_conferences_pool = ConferencesPool(
    message_coding=main_message_coding,
    gc_check_rate=CONFERENCE_GC_RATE,
    sync_canvas_and_member_ids=CONFERENCE_SYNC_MEMBER_AND_CANVAS_IDS,
    expiration_time_limit=CONFERENCE_EXPIRATION_TIME,
)
