"""
disclaimer: this is likely not secure and should not be heeded as an example for production use.
"""

import string
import secrets

import redis

from typing import Optional
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR
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
        cookies: Optional[str] = request.cookies.get("Authorization")
        if not cookies:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        scheme, param = get_authorization_scheme_param(cookies)
        if scheme.lower() != "bearer":
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
                if 'name' in s:
                    return s['name']
                else:
                    raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to obtain user")
            except Exception as e:
                print("exception", e)
                raise e


cookie_auth = CookieAuth(auto_error=True)
