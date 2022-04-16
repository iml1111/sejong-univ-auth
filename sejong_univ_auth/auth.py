from typing import Type, Optional, Union, List
from .method import Manual, METHODS
from .authenticator import Authenticator, AuthResponse
from .exceptions import InvalidMethod

method_hint = Optional[
    Union[
        Type[Authenticator],
        List[Type[Authenticator]]
    ]
]

def auth(
    id: str,
    password: str,
    methods: method_hint = Manual
) -> AuthResponse:
    if (
        isinstance(methods, list)
        and all([method.__bases__[0] is Authenticator for method in methods])
    ):
        failed_responses = []
        for method in methods:
            response: AuthResponse = method().authenticate(id, password)
            if response.is_auth:
                return response
            failed_responses.append(response)
        return failed_responses

    elif methods.__bases__[0] is Authenticator:
        return methods().authenticate(id, password)

    else:
        raise InvalidMethod()
