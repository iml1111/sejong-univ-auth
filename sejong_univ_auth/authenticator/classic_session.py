"""대양휴머니티칼리지 세션을 통한 로그인 검증"""
import requests
from bs4 import BeautifulSoup as bs
from sejong_univ_auth.authenticator import Authenticator, AuthResponse
from sejong_univ_auth.decorator import timeout_handler


class ClassicSession(Authenticator):

    @timeout_handler
    def authenticate(self, id: str, password: str) -> AuthResponse:
        res = self._session_request(id, password)
        if res.status_code == 200:
            soup = bs(res.text, 'html.parser')
            soups = soup.select(
                'div.contentWrap > ul.tblA > li > dl > dd')
            if not soups:
                return self._auth_failed(is_auth=False)
            major = soups[0].get_text().strip()
            name = soups[2].get_text().strip()
            grade = soups[3].get_text().strip()
            status = soups[4].get_text().strip()
            return self._success(
                body={
                    'name': name,
                    'major': major,
                    'grade': grade,
                    'status': status,
                }
            )
        else:
            return self._unknown_server_error(
                status_code=response.status_code
            )


    def _session_request(self, id: str, password: str):
        with requests.session() as s:
            res = s.get(
                'http://classic.sejong.ac.kr/',
                headers=self.header,
                timeout=self.timeout_sec
            )
            res = s.post(
                'https://classic.sejong.ac.kr/userLogin.do',
                data={'userId': id, 'password': password},
                headers=self.header,
                timeout=self.timeout_sec
            )
            return s.get(
                url=(
                    'https://classic.sejong.ac.kr/'
                    'userCertStatus.do?menuInfoId=MAIN_02_05'
                ),
                headers=self.header,
                timeout=self.timeout_sec
            )


if __name__ == '__main__':
    pass

