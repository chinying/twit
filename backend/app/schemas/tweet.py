from pydantic import BaseModel


class PostTweetInput(BaseModel):
    message: str


class BaseTweet(BaseModel):
    message: str
    author_id: str


class TweetCreate(BaseTweet):
    pass
