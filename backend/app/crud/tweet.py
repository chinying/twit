from app import models
from app.schemas.tweet import TweetCreate
from databases import Database
from sqlalchemy.orm import Session


class Tweet:
    def __init__(self):
        self.model = models.Tweet

    def create_tweet(self, db: Session, tweet: TweetCreate) -> models.Tweet:
        new_tweet = self.model(message=tweet.message, author_id=tweet.author_id)
        db.add(new_tweet)
        db.commit()
        db.refresh(new_tweet)
        return new_tweet


tweet = Tweet()
