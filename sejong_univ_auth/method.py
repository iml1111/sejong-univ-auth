from .authenticator import (
    Authenticator, AUTHENTICATORS,
    PortalSSOToken, DosejongSession,
    AuthResponse
)


Manual = AUTHENTICATORS

METHODS = (Manual, PortalSSOToken, DosejongSession)
