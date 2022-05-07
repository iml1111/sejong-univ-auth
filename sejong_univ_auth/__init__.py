"""
Sejong-Univ-Auth
"""

import requests, bs4
from .auth import auth
from .method import (
    METHODS,
    Manual,
    PortalSSOToken,
    DosejongSession,
    MoodlerSession,
    ClassicSession,
)


__AUTHOR__ = "IML"
__VERSION__ = "0.3.2"