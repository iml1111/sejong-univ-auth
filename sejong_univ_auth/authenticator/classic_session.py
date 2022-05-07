"""대양휴머니티칼리지 세션을 통한 로그인 검증"""
import requests
from bs4 import BeautifulSoup as bs
from bs4.element import PageElement
from sejong_univ_auth.authenticator import Authenticator, AuthResponse
from sejong_univ_auth.decorator import timeout_handler
from sejong_univ_auth.exceptions import AuthFailed, ParseError


class ClassicSession(Authenticator):

    @timeout_handler
    def authenticate(self, id: str, password: str) -> AuthResponse:
        try:
            res = self._session_request(id, password)
            if res.status_code == 200:
                userinfo: dict = self._get_userinfo(res.text)
                return self._success(body=userinfo)
            else:
                return self._unknown_server_error(
                    status_code=res.status_code
                )
        except AuthFailed:
            return self._auth_failed(
                is_auth=False,
                body={
                    'message': "아이디 및 비밀번호가 일치하지 않습니다."
                }
            )
        except Exception:
            return self._unknown_issue()

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
            soup = bs(res.text, 'html.parser')
            soup = soup.select_one('p.tc')
            if soup is None:
                return s.get(
                    url=(
                        'https://classic.sejong.ac.kr/'
                        'userCertStatus.do?menuInfoId=MAIN_02_05'
                    ),
                    headers=self.header,
                    timeout=self.timeout_sec
                )
            else:
                text = self.convert_text(soup)
                if text == '로그인 정보가 올바르지 않습니다.':
                    raise AuthFailed()
                else:
                    raise ParseError(expected=False)
    
    def _get_userinfo(self, content: str):
        soup = bs(content, 'html.parser')
        t = self.convert_text

        # 사용자 기본 정보 조회
        soups = soup.select(
            'div.contentWrap > ul.tblA > li > dl > dd')
        major = t(soups[0])
        name = t(soups[2])
        grade = t(soups[3])
        status = t(soups[4])

        # 고전 독서 인증 현황 정보 조회
        soup = soup.select_one('table.listA')
        key_soups = soup.select('thead > tr > th')
        value_soups = soup.select('tbody > tr > td')
        read_certification = {
            t(key): t(value) 
            for key, value in zip(
                key_soups[1:5], 
                value_soups[1:5], 
            )
        }

        return {
            'major': major,
            'name': name,
            'grade': grade,
            'status': status,
            'read_certification': read_certification,
        }

    @staticmethod
    def convert_text(soup: PageElement) -> str:
        return soup.get_text().strip()


if __name__ == '__main__':
    pass

