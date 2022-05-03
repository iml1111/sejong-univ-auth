from .authenticator import (
    Authenticator,
    AUTHENTICATORS,
    AuthResponse
)
from .authenticator import (
    PortalSSOToken,
    DosejongSession,
    MoodlerSession,
)


Manual = AUTHENTICATORS

METHODS = (Manual, PortalSSOToken, DosejongSession)
