from email_validator import (
    validate_email,
    EmailNotValidError,
    EmailSyntaxError,
    EmailUndeliverableError,
)


def is_email(a: str):
    try:
        validate_email(a)
        return True
    except EmailNotValidError:
        return False
