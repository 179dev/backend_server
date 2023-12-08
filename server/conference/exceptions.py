class ConferenceNotFound(Exception):
    pass


class ConferenceControllerError(Exception):
    pass


class ForbiddenConferenceActionError(Exception):
    pass


class ConferenceValidationError(ConferenceControllerError):
    pass
