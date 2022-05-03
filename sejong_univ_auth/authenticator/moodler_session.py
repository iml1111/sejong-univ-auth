"""
SJULMS 로그인 로직
"""
import requests
from bs4 import BeautifulSoup as bs
from sejong_univ_auth.authenticator import Authenticator, AuthResponse
from sejong_univ_auth.decorator import timeout_handler


class MoodlerSession(Authenticator):

    @timeout_handler
    def authenticate(self, id: str, password: str) -> AuthResponse:

        res = self.request(
            url="https://sjulms.moodler.kr/login/index.php",
            data={
                'username': id,
                'password': password
            }
        )
        if res.status_code == 200:
            soup = bs(res.text, 'html.parser') \
                .select_one('div.user-info-picture')
            if soup is None:
                return self._auth_failed(is_auth=False)
            name = soup.select_one('h4')
            major = soup.select_one('p.department')
            if not name or not major:
                return self._unknown_issue()
            return self._success(
                body={
                    'name': name.get_text().strip(),
                    'major': major.get_text().strip()
                }
            )
        else:
            return self._unknown_server_error(
                status_code=res.status_code
            )

if __name__ == '__main__':
    pass



