import enum


class Status(enum.Enum):
    """
        These statuses enums we can use for USER Approval status
        And DOCUMENT status
    """
    APPROVED = 'APPROVED'
    PENDING = 'PENDING'
    REJECTED = 'REJECTED'
