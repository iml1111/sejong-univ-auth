

class InvalidMethod(Exception):

    def __str__(self) -> str:
        return '"methods" argument must be a single object that inherits from the "Authenticator" class or a list.'


class ParseError(Exception):

    def __init__(self, expected: bool = False):
        """
        # expected
        - true: 파싱에는 실패했지만, 모듈이 예상하고 있는 에러임. 
            - 대처 가능한 리스폰스 반환
        - false: 모듈이 예상하지 못한 부분에서 파싱 실패.
        """
        self.expected = expected

    def __str__(self) -> str:
        if self.expected:
            return "Failed parse user resourse."
        else:
            return "Unknown Website Structure."


class AuthFailed(Exception):

    def __str__(self) -> str:
        return 'Authentication Failed.'
