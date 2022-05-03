from .authenticator import (
    Authenticator,
    AUTHENTICATORS,
    AuthResponse
)
from .authenticator import *

# 모든 Authenticator를 순차적으로 수행합니다.
Manual = AUTHENTICATORS

METHODS = (
    Manual,
    PortalSSOToken,
    DosejongSession,
    ClassicSession
)
