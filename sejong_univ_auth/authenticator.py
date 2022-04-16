from abc import ABCMeta, abstractmethod
from collections import namedtuple
import requests
from bs4 import BeautifulSoup as bs
from requests.exceptions import Timeout
from .config import USER_AGENT, TIMEOUT_SEC
from .decorator import header


AuthResponse = namedtuple(
    'AuthResponse', [
        'is_auth', # bool
        'code', # str
        'body', # Any
    ]
)

FailedResponse = namedtuple(
    'FailedResponse', [
        'status_code', # int
        'headers' # dict
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
            return FailedResponse(500, {})

    @abstractmethod
    def authenticate(self, id: str, password: str) -> AuthResponse:
        pass


class PortalSSOToken(Authenticator):
    """Portal to BlackBoard ssotoken 생성 유무 검증"""

    @header('Referer', "https://portal.sejong.ac.kr")
    def authenticate(self, id: str, password: str) ->AuthResponse:
        response = self.request(
            url='https://portal.sejong.ac.kr/jsp/login/login_action.jsp',
            data={
                'mainLogin': 'Y',
                'rtUrl': 'blackboard.sejong.ac.kr',
                'id': id,
                'password': password,
            }
        )
        if response.status_code == 200:
            if 'ssotoken' in response.headers.get('Set-Cookie', ''):
                return AuthResponse(is_auth=True, code='success', body=None)
            else:
                return AuthResponse(
                    is_auth=False, code='auth_failed', body={
                    'message': '계정 정보가 잘못되었거나, 인증 포맷 자체에 문제가 있습니다.'
                })
        else:
            return AuthResponse(
                is_auth=False, code='unknown_server_error', body={
                'message': (
                    '인증 서버가 200(OK)를 반환하지 않아, '
                    '인증 결과를 조회할 수 없습니다.')
            })


class DosejongSession(Authenticator):

    def authenticate(self, id: str, password: str) -> AuthResponse:
        response = self._session_request(id, password)
        print()
        if response.status_code == 200:
            soup = bs(response.text, 'html.parser')
            soup = soup.select('div.info')
            if not soup:
                return AuthResponse(
                    is_auth=False, code='auth_failed', body={
                    'message': '계정 정보가 잘못되었거나, 인증 포맷 자체에 문제가 있습니다.'
                })
            return AuthResponse(
                is_auth=True, code='success', body={
                'name': soup[0].find('b').get_text().strip(),
                'major': soup[0].find("small").get_text().strip().split(" ")[1],
            })
        else:
            return AuthResponse(
                is_auth=False, code='unknown_server_error', body={
                'message':(
                    '인증 서버가 200(OK)를 반환하지 않아, '
                    '인증 결과를 조회할 수 없습니다.')
            })

    def _session_request(self, id: str, password: str):
        try:
            with requests.session() as s:
                s.post(
                    url="https://do.sejong.ac.kr/ko/process/member/login",
                    headers=self.header,
                    timeout=self.timeout_sec,
                    data={'email': id, 'password': password}
                )
                return s.get('https://do.sejong.ac.kr/')
        except Timeout:
            return FailedResponse(500, {})
