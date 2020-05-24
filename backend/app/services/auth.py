"""
disclaimer: this is likely not secure and should not be heeded as an example for production use.
"""

import string
import secrets

import redis

from typing import Optional
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from fastapi import HTTPException
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param

from app.services.jwt import verify_jwt

r = redis.Redis(host="localhost", port=6379, db=0)
alphabet = string.digits + string.ascii_letters
PREFIX = "twit_user"


def generate_otp() -> str:
    return "".join(secrets.choice(string.digits) for i in range(6))


def generate_otp_for_user(user: str):
    otp = generate_otp()
    r.set(f"{PREFIX}_{user}", otp, ex=600)
    return otp


def verify_otp(user: str, otp: str) -> bool:
    result = r.get(f"{PREFIX}_{user}")
    if result:
        # TODO: evict key after login success
        return result.decode("utf-8") == otp
    else:
        return False


def generate_session_key() -> str:
    return "".join(secrets.choice(alphabet) for i in range(20))


class CookieAuth(SecurityBase):
    def __init__(self, scheme_name: str = None, auto_error: bool = True):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        print("invoked")
        cookies: str = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(cookies)
        if not cookies or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        else:
            try:
                s = verify_jwt(param)
                print("success", s)
                return s
            except Exception as e:
                print("exception", e)
                raise e


cookie_auth = CookieAuth(auto_error=True)
