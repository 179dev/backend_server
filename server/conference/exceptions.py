class ConferenceNotFound(Exception):
    pass


class ConferenceControllerError(Exception):
    pass


class ForbiddenConferenceAction(Exception):
    pass


class ConferenceValidationError(ConferenceControllerError):
    pass
