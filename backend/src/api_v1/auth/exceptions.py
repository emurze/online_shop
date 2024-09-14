class UserNameAlwaysExistsException(Exception):
    pass


class UserEmailAlwaysExistsException(Exception):
    pass


class UserNotActiveException(Exception):
    pass


class UserPasswordNotVerifiedException(Exception):
    pass


class UserNotFoundException(Exception):
    pass
