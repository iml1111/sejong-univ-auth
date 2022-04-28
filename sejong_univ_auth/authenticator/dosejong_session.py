"""Dosejong 세션을 통한 로그인 검증"""
import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup as bs
from sejong_univ_auth.authenticator import Authenticator, AuthResponse


class DosejongSession(Authenticator):

    def authenticate(self, id: str, password: str) -> AuthResponse:
        response = self._session_request(id, password)
        if response.status_code == 200:
            soup = bs(response.text, 'html.parser')
            soup = soup.select('div.info')
            if not soup:
                return self._auth_failed(is_auth=False)
            return self._success(
                body={
                    'name': soup[0].find('b').get_text().strip(),
                    'major': soup[0].find("small").get_text().strip().split(" ")[1],
                }
            )
        else:
            return self._unknown_server_error(status_code=response.status_code)

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
            return self._timeout()