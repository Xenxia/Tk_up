class Error(Exception):
    """Base class for other exceptions"""
    pass


class IdNotExist(Error):
    """Raised when not found ID"""
    pass