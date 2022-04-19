from sejong_univ_auth.authenticator import Authenticator, AuthResponse
from sejong_univ_auth.decorator import header


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
                return self._success()
            else:
                return self._auth_failed()
        else:
            return self._unknown_server_error(status_code=response.status_code)