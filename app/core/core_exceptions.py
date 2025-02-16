class CommonException(Exception):
    def __int__(self, message: str):
        self.message = message
        super().__init__(message)


class UnauthorizedException(CommonException):
    def __int__(self, message):
        super().__int__(message)


class InvalidRequestException(CommonException):
    def __int__(self, message):
        super().__int__(message)


class NotFoundException(CommonException):
    def __int__(self, message):
        super().__int__(message)


class ConflictException(CommonException):
    def __int__(self, message):
        super().__int__(message)


class NotAcceptable(CommonException):
    def __int__(self, message):
        super().__int__(message)
