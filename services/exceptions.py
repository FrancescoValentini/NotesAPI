class ServiceError(Exception):
    pass


class UserAlreadyExistsError(ServiceError):
    pass


class InvalidCredentialsError(ServiceError):
    pass


class UserNotFoundError(ServiceError):
    pass


class NoteNotFoundError(ServiceError):
    pass