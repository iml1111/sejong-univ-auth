"""대양휴머니티칼리지 세션을 통한 로그인 검증"""
import requests
from bs4 import BeautifulSoup as bs
from bs4.element import PageElement
from sejong_univ_auth.authenticator import Authenticator, AuthResponse
from sejong_univ_auth.decorator import timeout_handler
from sejong_univ_auth.exceptions import ParseError


class ClassicSession(Authenticator):

    @timeout_handler
    def authenticate(self, id: str, password: str) -> AuthResponse:
        res = self._session_request(id, password)
        if res.status_code == 200:
            try:
                userinfo: dict = self._get_userinfo(res.text)
            except ParseError as e:
                if e.expected:
                    return self._auth_failed(is_auth=False)
                else:
                    return self._unknown_issue()
            except Exception:
                return self._unknown_issue()
            
            return self._success(body=userinfo)
        else:
            return self._unknown_server_error(
                status_code=res.status_code
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
    
    def _get_userinfo(self, content: str):
        soup = bs(content, 'html.parser')

        # 사용자 기본 정보 조회
        soups = soup.select(
            'div.contentWrap > ul.tblA > li > dl > dd')
        if not soups:
            raise ParseError(expected=True)
        t = self.convert_text

        major = t(soups[0])
        name = t(soups[2])
        grade = t(soups[3])
        status = t(soups[4])

        # 고전 독서 인증 현황 정보
        soup = soup.select_one('table.listA')
        if not soups:
            raise ParseError(expected=True)
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

