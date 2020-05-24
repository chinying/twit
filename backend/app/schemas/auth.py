from pydantic import BaseModel


class RequestOTPInput(BaseModel):
    email: str


class VerifyOTPInput(BaseModel):
    email: str
    otp: str
