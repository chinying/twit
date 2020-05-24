"""
disclaimer: this is likely not secure and should not be heeded as an example for production use.
"""

import string
import secrets

import redis

r = redis.Redis(host="localhost", port=6379, db=0)
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
