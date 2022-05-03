"""Portal to BlackBoard ssotoken 생성 유무 검증"""
import re

from sejong_univ_auth.authenticator import Authenticator, AuthResponse
from sejong_univ_auth.decorator import header, timeout_handler


class PortalSSOToken(Authenticator):

    @header('Referer', "https://portal.sejong.ac.kr")
    @timeout_handler
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
            ssotoken_exists = 'ssotoken' in response.headers.get('Set-Cookie', '')
            res_result = self._get_response_result(response.text)

            if ssotoken_exists:
                if res_result == 'OK':
                    return self._success()
                else:
                    return self._unknown_issue()
            else:
                if res_result in ('erridpwd', 'Error'):
                    return self._auth_failed(
                        is_auth=False,
                        prefix_code=res_result,
                        body={'message': '아이디 및 비밀번호가 일치하지 않습니다.'}
                    )
                elif res_result == 'pwsNeedChg':
                    return self._auth_failed(
                        is_auth=False,
                        prefix_code=res_result,
                        body={'message': '일정 횟수 이상 패스워드를 잘못 입력하여 계정이 잠겼습니다.'}
                    )
                elif res_result == 'invalidDt':
                    return self._auth_failed(
                        prefix_code=res_result,
                        body={'message': '접근 가능한 기간이 아닙니다.'}
                    )
                elif res_result == 'invalid':
                    return self._auth_failed(
                        is_auth=False,
                        prefix_code=res_result,
                        body={'message': '제한된 아이디입니다.'},
                    )
                elif res_result: # result 자체는 존재하나, 알 수 없음
                    return self._unknown_server_error(status_code=200)
                else: # result를 추출할 수 없음.
                    return self._unknown_issue()
        else:
            return self._unknown_server_error(
                status_code=response.status_code
            )

    @staticmethod
    def _get_response_result(response_text: str):
        pattern = re.search("var result = \'.*\';", response_text)
        return pattern.group()[14:-2] if pattern else None


if __name__ == '__main__':
    pass