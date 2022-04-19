from abc import ABCMeta, abstractmethod
from collections import namedtuple
import requests
from requests.exceptions import Timeout
from sejong_univ_auth.config import USER_AGENT, TIMEOUT_SEC


AuthResponse = namedtuple(
    'AuthResponse', [
        'success', # bool: 인증 정상 작동 여부
        'is_auth', # bool: 인증 여부
        'status_code', # bool: HTTP 통신 코드
        'code', # str: 반환 코드
        'body', # Any: 메타데이터
        'authenticator' # Class type: 사용된 Authenticator
    ]
)


class Authenticator(metaclass=ABCMeta):

    def __init__(
        self,
        timeout_sec: int = TIMEOUT_SEC
    ):
        self.header = {"User-Agent": USER_AGENT}
        self.timeout_sec = timeout_sec

    def request(self, url: str, data: dict):
        try:
            return requests.post(
                url=url, data=data,
                headers=self.header,
                timeout=self.timeout_sec,
            )
        except Timeout:
            return self._get_timeout_response()

    @abstractmethod
    def authenticate(self, id: str, password: str) -> AuthResponse:
        pass

    def _success(
        self, *, body=None, status_code=200
    ):
        return AuthResponse(
            success=True,
            is_auth=True,
            status_code=status_code,
            code='success',
            body=body or {},
            authenticator=self.__class__
        )

    def _auth_failed(
        self, *, body=None, status_code=200
    ):
        return AuthResponse(
            success=True,
            is_auth=False,
            status_code=status_code,
            code='auth_failed',
            body=body or {
                    'message': (
                        '계정 정보가 잘못되었거나, '
                        '인증 포맷 자체에 문제가 있습니다.')
                },
            authenticator=self.__class__
        )

    def _unknown_server_error(
        self, *, body=None, status_code=500
    ):
        return AuthResponse(
            success=True,
            is_auth=False,
            status_code=status_code,
            code='unknown_server_error',
            body=body or {
                'message': (
                    '인증 서버가 정상적인 결과가 반환하지 않아, '
                    '결과를 조회할 수 없습니다.')
            },
            authenticator=self.__class__
        )

    def _timeout(self):
        return AuthResponse(
            success=False,
            is_auth=False,
            status_code=None,
            code='timeout',
            body={'message': 'Timeout Exception Occured.'},
            authenticator=self.__class__
        )

# Custom Authenticators
from .portal_ssotoken import PortalSSOToken
from .dosejong_session import DosejongSession


AUTHENTICATORS = (PortalSSOToken, DosejongSession)
