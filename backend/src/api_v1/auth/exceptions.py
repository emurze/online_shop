class UserNameAlwaysExistsException(Exception):
    pass


class UserEmailAlwaysExistsException(Exception):
    pass


class UserNotAuthenticatedException(Exception):
    pass


class UserNotFoundException(Exception):
    pass
