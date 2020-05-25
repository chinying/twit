from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str


class UserCreate(BaseUser):
    pass
