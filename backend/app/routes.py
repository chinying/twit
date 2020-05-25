from fastapi import APIRouter, Depends, HTTPException, Response
from app.services.mail import send_local_mail
from app.services.auth import CookieAuth, cookie_auth, generate_session_key, verify_otp
from app.schemas.auth import RequestOTPInput, VerifyOTPInput

from sqlalchemy.orm import Session

from app.services.jwt import encode_cookie
from app.crud import user

from app.db import SessionLocal
from app.schemas.user import BaseUser, UserCreate

from app.config import COOKIE_DOMAIN

router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/")
def hello():
    return "hello world"


@router.post("/otp")
def get_otp(body: RequestOTPInput):
    send_local_mail(body.email)


# example of protected route
@router.get("/secret")
def secret_route(auth: CookieAuth = Depends(cookie_auth)):
    return "protected_route"


@router.post("/login")
def user_login(body: VerifyOTPInput, response: Response, db: Session = Depends(get_db)):
    authenticated = verify_otp(body.email, body.otp)

    if authenticated:
        user.get_or_create_user(db, UserCreate(email=body.email))

        session_key = encode_cookie(body.email, generate_session_key())
        response.set_cookie(
            "Authorization",
            value=f"Bearer {session_key}",
            domain=COOKIE_DOMAIN,
            httponly=True,
            max_age=86400,  # seconds
        )
        return {"message": "auth success"}
    else:
        raise HTTPException(401)
