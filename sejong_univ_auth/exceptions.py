

class InvalidMethod(Exception):

    def __str__(self) -> str:
        return '"methods" argument must be a single object that inherits from the "Authenticator" class or a list.'


class ParseError(Exception):

    def __init__(self, expected: bool):
        self.expected = expected

    def __str__(self) -> str:
        if self.expected:
            return "Failed parse user resourse."
        else:
            return "Unknown Website Structure."