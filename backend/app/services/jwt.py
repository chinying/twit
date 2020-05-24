from jose import jwt
from app.config import JWT_SECRET


def encode_cookie(user: str, session: str):
    return jwt.encode(
        {"iss": "twit", "sub": f"user_session_{session}", "name": user},
        JWT_SECRET,
        algorithm="HS256",
    )


def verify_jwt(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
