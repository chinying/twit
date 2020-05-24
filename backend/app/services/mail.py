import os
import cgi

# this is a bad hack to monkey-patch a deprecated, unused method
# @see: https://github.com/marrow/mailer/issues/87
cgi.parse_qsl = {}
from marrow.mailer import Mailer, Message

from app.services.auth import generate_otp_for_user


def send_local_mail(user: str):
    mailer = Mailer(dict(transport=dict(use="sendmail", host="localhost")))
    mailer.start()

    otp = generate_otp_for_user(user)
    print(otp)

    message = Message(author="noreply@chinying.com", to=user)
    message.sendmail_f = "noreply@chinying.com"
    message.subject = "Login for Twit"
    message.plain = f"Your OTP is {otp}"
    mailer.send(message)

    mailer.stop()
