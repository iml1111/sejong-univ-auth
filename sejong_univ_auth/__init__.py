import requests, bs4
from .auth import auth
from .method import (
    METHODS,
    Manual,
    PortalSSOToken,
    DosejongSession,
)


__AUTHOR__ = "IML"
__VERSION__ = "0.1.1"