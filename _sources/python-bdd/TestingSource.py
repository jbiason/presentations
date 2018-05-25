import mainsource


class TestingSource(object):
    def __init__(self):
        self.username = None
        self.password = None
        self.last_exception = None

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def create_user(self):
        try:
            mainsource.create_user(self.username, self.password)
        except mainsource.UserCreationError as exc:
            self.last_exception = exc

    def is_invalid_password(self):
        return (self.last_exception and
                isinstance(self.last_exception,
                           mainsource.PasswordIsNotStrongEnough))
