from fastapi import APIRouter
from app.services.mail import send_local_mail
from app.services.auth import verify_otp
from app.schemas.auth import RequestOTPInput, VerifyOTPInput

router = APIRouter()


@router.get("/")
def hello():
    return "hello world"


@router.post("/otp")
def get_otp(body: RequestOTPInput):
    send_local_mail(body.email)


@router.post("/login")
def user_login(body: VerifyOTPInput):
    authenticated = verify_otp(body.email, body.otp)
    if authenticated:
        return "auth success"
    else:
        return "auth failure"
