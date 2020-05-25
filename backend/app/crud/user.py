from app import models
from app.schemas.user import UserCreate
from databases import Database
from sqlalchemy.orm import Session


class User:
    def __init__(self):
        self.model = models.User

    def get_or_create_user(self, db: Session, user: UserCreate) -> User:
        try:
            return db.query(self.model).filter(self.model.email == user.email).one()
        except Exception as e:
            print(e)

            new_user = self.model(email=user.email)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user


user = User()
