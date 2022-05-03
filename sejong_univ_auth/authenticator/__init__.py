"""
Base Authenticator
"""
from abc import ABCMeta, abstractmethod
from collections import namedtuple
import requests
from sejong_univ_auth.config import USER_AGENT, TIMEOUT_SEC


AuthResponse = namedtuple(
    'AuthResponse', [
        'success', # bool: 인증 서버 정상 동작 여부
        'is_auth', # bool or None: 인증 여부
            # (True: 인증 성공)
            # (False: 인증 실패)
            # (None: 인증 확인 불가능)
        'status_code', # int: HTTP 통신 코드
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
        return requests.post(
            url=url, 
            data=data,
            headers=self.header,
            timeout=self.timeout_sec,
        )

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
            authenticator=self.__class__.__name__
        )

    def _auth_failed(
        self, *,
        is_auth=None,
        body=None,
        status_code=200,
        prefix_code='',
    ):
        return AuthResponse(
            success=True,
            is_auth=is_auth,
            status_code=status_code,
            code=prefix_code + "_auth_failed" if prefix_code else 'auth_failed',
            body=body or {
                    'message': (
                        '계정 정보가 잘못되었거나, '
                        '인증 포맷 자체에 문제가 있습니다.')
                },
            authenticator=self.__class__.__name__
        )

    def _unknown_issue(
        self, *, body=None, status_code=200,
    ):
        return AuthResponse(
            success=True,
            is_auth=None,
            status_code=status_code,
            code='unknown_issue',
            body=body or {
                    'message': (
                        '예상된 포맷과 다릅니다. 관리자에게 문의해주세요!'
                        '[https://github.com/iml1111/sejong-univ-auth/issues]')
                },
            authenticator=self.__class__.__name__
        )

    def _unknown_server_error(
        self, *, body=None, status_code=500
    ):
        return AuthResponse(
            success=False,
            is_auth=None,
            status_code=status_code,
            code='unknown_server_error',
            body=body or {
                'message': (
                    '인증 서버가 정상적인 결과가 반환하지 않아, '
                    '결과를 조회할 수 없습니다.')
            },
            authenticator=self.__class__.__name__
        )

    def _timeout(self):
        return AuthResponse(
            success=False,
            is_auth=None,
            status_code=None,
            code='timeout',
            body={'message': 'Timeout Exception Occured.'},
            authenticator=self.__class__.__name__
        )

# Custom Authenticators
from .portal_ssotoken import PortalSSOToken
from .dosejong_session import DosejongSession
from .moodler_session import MoodlerSession
from .classic_session import ClassicSession

# Average Fastest Order
AUTHENTICATORS = (
    PortalSSOToken,
    ClassicSession,
    MoodlerSession,
    DosejongSession,
)
