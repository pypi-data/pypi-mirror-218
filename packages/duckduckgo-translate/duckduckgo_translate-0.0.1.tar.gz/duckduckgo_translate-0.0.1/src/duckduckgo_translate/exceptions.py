class TranslatorException(Exception):
    """Base exception for this script.

    :note: This exception should not be raised directly."""
    pass


class BadResponseException(TranslatorException):
    pass

class ConnectionException(TranslatorException):
    pass

class QueryReturnedNotFoundException(TranslatorException):
    pass

class TooManyRequestsException(TranslatorException):
    pass
