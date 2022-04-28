

class InvalidMethod(Exception):

    def __str__(self):
        return '"methods" argument must be a single object that inherits from the "Authenticator" class or a list.'