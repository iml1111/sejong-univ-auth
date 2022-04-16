from .authenticator import (
    Authenticator, AUTHENTICATORS,
    PortalSSOToken, DosejongSession,
    AuthResponse
)


class Manual(Authenticator):
    """
    모든 Authenticator를 순서대로 실행.
    성공시, 가장 먼저 성공한 리스폰스를 반환.
    실패시, 모든 실패한 리스폰스 정보를 리스트로 반환.
    """

    def authenticate(self, id: str, password: str) -> AuthResponse:
        failed_responses = []
        for method in AUTHENTICATORS:
            auth = method()
            response = auth.authenticate(id, password)
            if response.is_auth:
                return response
            failed_responses.append(response)

        return failed_responses


METHODS = (Manual, PortalSSOToken, DosejongSession)
