"""
Main Module
"""
from collections.abc import Iterable
from typing import Type, Optional, Union, List, Tuple
from .method import Manual
from .authenticator import Authenticator, AuthResponse
from .exceptions import InvalidMethod

method_hint = Optional[Union[
    Type[Authenticator],
    Iterable[Type[Authenticator]],
]]

response_hint = Optional[Union[
    Type[AuthResponse],
    List[Type[AuthResponse]]
]]

def _validate_authenticator(authenticator) -> bool:
    return (
        hasattr(authenticator, '__bases__')
        and authenticator.__bases__[0] is Authenticator
    )


def auth(
    id: str,
    password: str,
    methods: method_hint = Manual
) -> response_hint:
    if (
        isinstance(methods, Iterable)
        and all([
            _validate_authenticator(method)
            for method in methods
        ])
    ):
        failed_responses = []
        for method in methods:
            response: AuthResponse = method().authenticate(id, password)
            if response.is_auth is not None:
                return response
            failed_responses.append(response)
        return failed_responses

    elif _validate_authenticator(methods):
        return methods().authenticate(id, password)

    else:
        raise InvalidMethod()
